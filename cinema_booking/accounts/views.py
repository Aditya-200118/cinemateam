from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
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


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        address_form = AddressForm(request.POST)
        card_form = CardForm(request.POST, is_registration=True)
        if user_form.is_valid() and address_form.is_valid() and card_form.is_valid():
            email = user_form.cleaned_data["email"]
            if get_user_model().objects.filter(email=email).exists():
                user_form.add_error("email", "Email already in use.")
                logger.warning("Email already in use: %s", email)
            else:
                try:
                    with transaction.atomic():
                        # Create Address instance
                        address = Address(
                            billing_address=address_form.cleaned_data[
                                "billing_address"
                            ],
                            city=address_form.cleaned_data["city"],
                            state=address_form.cleaned_data["state"],
                            zip_code=address_form.cleaned_data["zip_code"],
                        )
                        address.save()
                        logger.info("New address created: %s", address.billing_address)

                        # Create Customer instance and link to Address
                        customer = Customer(
                            first_name=user_form.cleaned_data["first_name"],
                            middle_name=user_form.cleaned_data["middle_name"],
                            last_name=user_form.cleaned_data["last_name"],
                            contact_no=user_form.cleaned_data["contact_no"],
                            email=user_form.cleaned_data["email"],
                            address=address,  # Link the address here
                        )
                        customer.set_password(user_form.cleaned_data["password"])
                        customer.save()
                        logger.info("New customer created: %s", customer.email)

                        # Create Card instance and link to Customer
                        card = Card(
                            customer=customer,
                            card_number=card_form.cleaned_data["card_number"],
                            expiry_date=card_form.cleaned_data["expiry_date"],
                            cvv=card_form.cleaned_data["cvv"],
                        )
                        card.save()
                        logger.info("Customer and card created successfully.")
                        return render(
                            request,
                            "accounts/register_done.html",
                            {"new_user": user_form},
                        )  # Render a success page. Will change to redirect later once things are fixed
                except Exception as e:
                    logger.error("Error during registration: %s", str(e))
                    user_form.add_error(
                        None, "An error occurred during registration. Please try again."
                    )
        else:
            logger.warning("User form errors: %s", user_form.errors)
            logger.warning("Address form errors: %s", address_form.errors)
            logger.warning("Card form errors: %s", card_form.errors)
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


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            token = get_random_string(20)
            user.reset_token = token
            user.save()
            reset_url = request.build_absolute_uri(f"/reset/{token}/")
            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_url}",
                "your-email@example.com",
                [email],
                fail_silently=False,
            )
            return redirect("password_reset_done")
    else:
        form = PasswordResetRequestForm()
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


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("home")
