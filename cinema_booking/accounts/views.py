from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.core.mail import send_mail
from django.conf import settings
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


from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.views import View

class CustomLogoutView(View):
    template_name = "accounts/logout_confirm.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Clear the session
        request.session.flush()
        return redirect('home')

class ConfirmLogoutView(LogoutView):
    next_page = "home"

    def dispatch(self, request, *args, **kwargs):
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
                    messages.error(request, "Disabled account")
            else:
                messages.error(request, "Invalid login")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


logger = logging.getLogger(__name__)


from django.core.mail import send_mail
from django.conf import settings

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
                            promotions=user_form.cleaned_data.get("promotions", False),  # Handle promotions opt-in
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

                        # Send confirmation email
                        send_mail(
                            'Registration Confirmation',
                            'Thank you for registering!',
                            settings.DEFAULT_FROM_EMAIL,
                            [customer.email],
                            fail_silently=False,
                        )
                        logger.info("Confirmation email sent to: %s", customer.email)

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


from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .models import User

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
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
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect("password_reset_done")
    else:
        form = PasswordResetForm()
    return render(request, "registration/password_reset_form.html", {"form": form})


from django.contrib.auth.forms import SetPasswordForm
from django.utils.crypto import get_random_string

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


from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from cryptography.fernet import InvalidToken, Fernet

@login_required
def edit_profile(request):
    user = request.user
    customer = Customer.objects.get(email=user.email)
    address = customer.address
    cards = customer.cards.all()

    # Decrypt card numbers
    fernet = Fernet(settings.ENCRYPTION_KEY)
    for card in cards:
        try:
            card.card_number = fernet.decrypt(card.card_number.encode()).decode()
        except InvalidToken:
            messages.error(request, "Failed to decrypt card information. Please contact support.")
            card.card_number = "Invalid"

    if request.method == "POST":
        profile_form = EditProfileForm(request.POST, instance=customer)
        address_form = AddressForm(request.POST, instance=address)

        if profile_form.is_valid() and address_form.is_valid():
            try:
                with transaction.atomic():
                    profile_form.save()
                    address_form.save()
                    # Send email notification (optional)
                    send_mail(
                        "Profile Updated",
                        "Your profile information has been updated.",
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    return redirect("profile")
            except Exception as e:
                logger.exception("Error during profile update: %s", str(e))
                messages.error(request, "An error occurred while updating your profile. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        profile_form = EditProfileForm(instance=customer)
        address_form = AddressForm(instance=address)

    context = {
        "profile_form": profile_form,
        "address_form": address_form,
    }
    return render(request, "accounts/edit_profile.html", context)




from django.contrib.auth.views import PasswordChangeView
# from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm
from django.shortcuts import render, get_object_or_404, redirect

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            
            # Send email notification
            send_mail(
                'Password Changed Successfully',
                'Your password has been changed successfully. If you did not make this change, please contact support immediately.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            
            return redirect('home')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer, Address, Card
from .forms import AddressForm, CardForm

@login_required
def profile_view(request):
    user = get_object_or_404(Customer, pk=request.user.pk)
    address_form = AddressForm(instance=user.address)
    card_form = CardForm()

    if request.method == 'POST':
        if 'address_form' in request.POST:
            address_form = AddressForm(request.POST, instance=user.address)
            if address_form.is_valid():
                address_form.save()
                return redirect('profile_view')
        elif 'card_form' in request.POST:
            card_form = CardForm(request.POST)
            if card_form.is_valid():
                card = card_form.save(commit=False)
                card.customer = user
                card.save()
                return redirect('profile_view')

    context = {
        'user': user,
        'address_form': address_form,
        'card_form': card_form,
    }
    return render(request, 'accounts/profile.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Card, Customer
from .forms import CardForm
from cryptography.fernet import InvalidToken, Fernet
from django.conf import settings

@login_required
def change_payment_method(request):
    user = request.user
    customer = Customer.objects.get(email=user.email)  # Ensure correct customer is fetched
    cards = customer.cards.all()  # Get all cards related to the customer

    # Decrypt card numbers for display
    fernet = Fernet(settings.ENCRYPTION_KEY)
    for card in cards:
        try:
            card.card_number = fernet.decrypt(card.card_number.encode()).decode()
        except InvalidToken:
            messages.error(request, "Failed to decrypt card information. Please contact support.")
            card.card_number = "Invalid"  # Set to Invalid if decryption fails

    if request.method == "POST":
        # Create forms for existing cards and the new card
        card_forms = [CardForm(request.POST, instance=card, prefix=f'card_{card.pk}') for card in cards]
        new_card_form = CardForm(request.POST, prefix='new_card')

        # Check if all card forms and the new card form are valid
        if all([cf.is_valid() for cf in card_forms]) and new_card_form.is_valid():
            try:
                with transaction.atomic():  # Ensure atomic transaction
                    # Save existing card forms
                    for cf in card_forms:
                        card = cf.save(commit=False)
                        card.customer = customer  # Explicitly assign the customer to the card
                        card.save()

                    # Handle new card creation if provided
                    if new_card_form.cleaned_data.get('card_number'):
                        new_card = new_card_form.save(commit=False)
                        new_card.customer = customer  # Assign customer to the new card
                        new_card.save()

                    # Success message and redirect
                    messages.success(request, "Payment methods updated successfully.")
                    return redirect("change_payment_method")
            except Exception as e:
                # Handle any error that occurred during saving
                messages.error(request, f"An error occurred while updating your payment methods: {str(e)}. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Instantiate forms for GET requests
        card_forms = [CardForm(instance=card, prefix=f'card_{card.pk}') for card in cards]
        new_card_form = CardForm(prefix='new_card')

    # Render the template with forms for existing cards and new card
    context = {
        "card_forms": card_forms,
        "new_card_form": new_card_form,
    }
    return render(request, "accounts/change_payment_method.html", context)