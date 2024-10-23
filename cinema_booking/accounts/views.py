from django.shortcuts import render

# Create your views here.
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import SetPasswordForm
from .forms import PasswordResetRequestForm
import string, random
from django.contrib.auth.hashers import make_password

from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from .models import Customer, Card, Address
from .forms import (
    LoginForm,
    UserRegistrationForm,
    CardForm,
    AddressForm,
    EditProfileForm,
)

from django.db import transaction
import logging

User = get_user_model()

from django.contrib.auth.views import LogoutView


class CustomLogoutView(LogoutView):
    next_page = "home"

    def dispatch(self, request, *args, **kwargs):
        # Clear the session
        request.session.flush()
        response = super().dispatch(request, *args, **kwargs)
        return redirect(self.next_page)


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                email=cd["email"],
                password=cd["password"],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Store user ID in session
                    request.session["user_id"] = user.user_id
                    # Redirect to home page
                    return redirect("home")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


logger = logging.getLogger(__name__)


def activate_account(request, uidb64, token):
    try:
        # UID decode
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("user_login")
    else:
        return render(request, "accounts/activation_invalid.html")


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        address_form = AddressForm(request.POST)
        card_form = CardForm(request.POST, is_registration=True)
        if user_form.is_valid() and address_form.is_valid() and card_form.is_valid():
            email = user_form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                user_form.add_error("email", "Email already in use.")
            else:
                with transaction.atomic():
                    # Address
                    address = address_form.save()

                    # Customer (is_active=False)
                    customer = Customer.objects.create(
                        first_name=user_form.cleaned_data["first_name"],
                        middle_name=user_form.cleaned_data.get("middle_name", ""),
                        last_name=user_form.cleaned_data["last_name"],
                        contact_no=user_form.cleaned_data["contact_no"],
                        email=email,
                        address=address,
                    )
                    customer.set_password(user_form.cleaned_data["password"])
                    customer.is_active = False
                    customer.save()

                    # email link
                    token = default_token_generator.make_token(customer)
                    uid = urlsafe_base64_encode(force_bytes(customer.pk))
                    activation_link = (
                        f"http://{request.get_host()}/accounts/activate/{uid}/{token}/"
                    )

                    subject = "Activate your BookMyTicket account"
                    message = (
                        f"Hello {customer.first_name},\n\n"
                        f"Thank you for registering at BookMyTicket.\n"
                        f"Please click the link below to activate your account:\n"
                        f"{activation_link}\n\n"
                        "If you did not register, please ignore this email.\n"
                    )

                    try:
                        send_mail(
                            subject, message, settings.DEFAULT_FROM_EMAIL, [email]
                        )
                    except Exception as e:
                        user_form.add_error(None, f"Error sending email: {str(e)}")

                    return render(request, "accounts/register_done.html")

    else:
        user_form = UserRegistrationForm()
        address_form = AddressForm()
        card_form = CardForm(is_registration=True)

    return render(
        request,
        "accounts/register.html",
        {"user_form": user_form, "address_form": address_form, "card_form": card_form},
    )


from django.http import HttpResponse


def test_session(request):
    request.session["test_key"] = "test_value"
    return HttpResponse("Session data stored.")


def check_session(request):
    value = request.session.get("test_key", "No session data found.")
    return HttpResponse(f"Session data: {value}")


from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import SetPasswordForm
from .forms import PasswordResetRequestForm

User = get_user_model()


def generate_temp_password(length=12):
    # random temparary passowrd
    return get_random_string(length)


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                # find user
                user = User.objects.get(email=email)

                # temp password security
                temp_password = generate_temp_password()
                hashed_password = make_password(temp_password)

                # save temp password at db
                user.password = hashed_password
                user.save()

                # sebd mail
                subject = "Temporary Password for Your Account"
                message = (
                    f"Hello {user.first_name},\n\n"
                    f"Your temporary password is: {temp_password}\n"
                    "Please log in and change your password immediately.\n\n"
                    "Thank you!"
                )
                try:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")

                return redirect("password_reset_done")

            except User.DoesNotExist:
                form.add_error("email", "No user with this email address exists.")
    else:
        form = PasswordResetForm()

    return render(request, "registration/password_reset_form.html", {"form": form})


def password_reset_confirm(request, token):
    try:
        user = User.objects.get(reset_token=token)
    except User.DoesNotExist:
        return redirect("password_reset_invalid")

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            user.reset_token = ""
            user.save()
            return redirect("password_reset_complete")
    else:
        form = SetPasswordForm(user)
    return render(request, "registration/password_reset_confirm.html", {"form": form})


def password_reset_done(request):
    return render(request, "registration/password_reset_done.html")


def password_reset_complete(request):
    return render(request, "registration/password_reset_complete.html")


@login_required
def edit_profile(request):
    user = request.user
    customer = Customer.objects.get(email=user.email)
    address = customer.address
    cards = customer.cards.all()

    if request.method == "POST":
        profile_form = EditProfileForm(request.POST, instance=customer)
        address_form = AddressForm(request.POST, instance=address)
        card_forms = [
            CardForm(request.POST, instance=card, is_registration=False)
            for card in cards
        ]

        if (
            profile_form.is_valid()
            and address_form.is_valid()
            and all([cf.is_valid() for cf in card_forms])
        ):
            profile_form.save()
            address_form.save()
            for cf in card_forms:
                cf.save()

            # email send
            send_mail(
                "Profile Updated Successfully",
                f"Hello {user.first_name}, your profile has been updated successfully.",
                "qkddlfkdrp@gmail.com",  # sender
                [user.email],  # reciever
                fail_silently=False,
            )

            return redirect("home")

    else:
        profile_form = EditProfileForm(instance=customer)
        address_form = AddressForm(instance=address)
        card_forms = [CardForm(instance=card, is_registration=False) for card in cards]

    context = {
        "profile_form": profile_form,
        "address_form": address_form,
        "card_forms": card_forms,
    }
    return render(request, "accounts/edit_profile.html", context)


from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("home")
