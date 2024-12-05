# accounts/views/customer_views.py

from . import *
import logging
from django.contrib.auth.views import LogoutView
from accounts.services.card_facade import CardFacade  # Updated to use CardFacade
from accounts.services.user_profile_facade import UserProfileFacade  # Added facade import
from accounts.services.email_proxy import EmailProxy, DjangoEmailService
from django.utils.decorators import method_decorator
from django.contrib import messages
logger = logging.getLogger(__name__)
from django.contrib.auth import logout
from django.views import View


# class CustomLogoutView(View):
#     template_name = "accounts/logout_confirm.html"

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         # Clear the session
#         request.session.flush()
#         return redirect('home')

# class ConfirmLogoutView(LogoutView):
#     next_page = "home"
#     def dispatch(self, request, *args, **kwargs):
#         response = super().dispatch(request, *args, **kwargs)
#         return redirect(self.next_page)
    
@method_decorator(login_required, name='dispatch')
class CustomLogoutView(View):
    template_name = "accounts/logout_confirm.html"
    next_page = "home"

    def get(self, request, *args, **kwargs):
        # Set headers to prevent caching
        response = render(request, self.template_name)
        # force remove any cache
        # response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        # response['Pragma'] = 'no-cache'
        # response['Expires'] = '0'
        return response

    def post(self, request, *args, **kwargs):
        logout(request)
        response = redirect(self.next_page)
        # response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        # response['Pragma'] = 'no-cache'
        # response['Expires'] = '0'
        return redirect(self.next_page)
    
def user_login(request):
    error_message = None
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
                    error_message = "Disabled account"
            else:
                if not get_user_model().objects.filter(email=cd["email"]).exists():
                    error_message = "Invalid email"
                else:
                    error_message = "Invalid password"
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form, "error_message": error_message})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user_model = get_user_model()  
        user = user_model.objects.get(pk=uid)  
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  
        user.save()
        return redirect('user_login') 
    else:
        return render(request, 'accounts/activation_invalid.html')
    


def register(request):

    email_service = EmailProxy(DjangoEmailService())

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
                        # Create UserProfileFacade instance
                        user_profile_facade = UserProfileFacade()

                        # Extract user and address data
                        address_data = {
                            "billing_address": address_form.cleaned_data["billing_address"],
                            "city": address_form.cleaned_data["city"],
                            "state": address_form.cleaned_data["state"],
                            "zip_code": address_form.cleaned_data["zip_code"],
                        }

                        profile_data = {
                            "middle_name": user_form.cleaned_data["middle_name"],
                            "contact_no": user_form.cleaned_data["contact_no"],
                            "promotions": user_form.cleaned_data.get("promotions", False),
                        }

                        # Create customer with profile and address via facade
                        customer = user_profile_facade.create_customer(
                            email=email,
                            password=user_form.cleaned_data["password"],
                            first_name=user_form.cleaned_data["first_name"],
                            last_name=user_form.cleaned_data["last_name"],
                            profile_data=profile_data,
                            address_data=address_data,
                        )

                        # Create CardFacade instance and link card to customer
                        card_facade = CardFacade()
                        card_data = {
                            "card_name": card_form.cleaned_data["card_name"],
                            "card_number": card_form.cleaned_data["card_number"],
                            "expiry_date": card_form.cleaned_data["expiry_date"],
                            "cvv": card_form.cleaned_data["cvv"],
                        }
                        card = card_facade.add_card(customer, card_data)  # Link card to customer
                        logger.info("Customer and card created successfully.")

                        # Send activation email
                        token = default_token_generator.make_token(customer)
                        uid = urlsafe_base64_encode(force_bytes(customer.pk))
                        activation_link = f"http://{request.get_host()}/accounts/activate/{uid}/{token}/"
                        
                        # Prepare confirmation email
                        subject = "Activate your BookMyTicket account"
                        message = (
                            f"Hello {customer.first_name},\n\n"
                            f"Thank you for registering at BookMyTicket.\n"
                            f"Please click the link below to activate your account:\n"
                            f"{activation_link}\n\n"
                            "If you did not register, please ignore this email.\n"
                        )

                        try:
                            email_service.send_email(subject, message, [email])
                            logger.info(f"Activation email sent to {email}")
                        except Exception as e:
                            user_form.add_error(None, f"Error sending email: {str(e)}")
                            logger.error(f"Email sending failed: {str(e)}")

                        return render(
                            request,
                            "accounts/register_done.html",
                            {"new_user": user_form},
                        )  # Render a success page.
                except Exception as e:
                    logger.error("Error during registration: %s", str(e))
                    user_form.add_error(None, "An error occurred during registration. Please try again.")
                    messages.error(request, "An error occurred during registration. Please try again.")
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


from django.http import JsonResponse

def check_email_exists(request):
    if request.method == "GET":
        email = request.GET.get("email", None)
        if email:
            exists = get_user_model().objects.filter(email=email).exists()
            return JsonResponse({"exists": exists})
    return JsonResponse({"exists": False}, status=400)