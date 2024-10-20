from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
import logging
from django.http import HttpResponse
from .models import Customer, Card
from .forms import LoginForm, UserRegistrationForm, CardForm

logger = logging.getLogger(__name__)

# **Email activation view**
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        logger.info(f"User {user.email} activated successfully.")
        return redirect('user_login')
    else:
        return render(request, 'accounts/activation_invalid.html')

# **Email sending function**
def send_activation_email(customer, request):
    uidb64 = urlsafe_base64_encode(force_bytes(customer.pk))
    token = default_token_generator.make_token(customer)
    activation_link = request.build_absolute_uri(
        reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
    )

    email_subject = 'Activate Your Account'
    email_body = render_to_string('accounts/activation_email.html', {
        'activation_link': activation_link,
        'user': customer,
    })

    try:
        send_mail(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [customer.email],
            fail_silently=False,
        )
        logger.info(f"Activation email sent to {customer.email}")
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")

# **Registration view**
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        card_form = CardForm(request.POST)
        if user_form.is_valid() and card_form.is_valid():
            try:
                with transaction.atomic():
                    # Create user
                    customer = get_user_model().objects.create_user(
                        first_name=user_form.cleaned_data['first_name'],
                        middle_name=user_form.cleaned_data['middle_name'],
                        last_name=user_form.cleaned_data['last_name'],
                        contact_no=user_form.cleaned_data['contact_no'],
                        email=user_form.cleaned_data['email'],
                        billing_address=user_form.cleaned_data['billing_address'],
                        city=user_form.cleaned_data['city'],
                        state=user_form.cleaned_data['state'],
                        zip_code=user_form.cleaned_data['zip_code'],
                        password=user_form.cleaned_data['password'],
                        is_active=False,  # Deactivate account
                    )
                    logger.info(f"New customer created: {customer.email}")

                    # Generate UID and Token
                    uidb64 = urlsafe_base64_encode(force_bytes(customer.pk))
                    token = default_token_generator.make_token(customer)

                    # Create URL
                    activation_link = request.build_absolute_uri(
                        reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
                    )

                    logger.info(f"UID: {uidb64}, Token: {token}")
                    logger.info(f"Activation Link: {activation_link}")

                    # Send email
                    send_mail(
                        'Activate Your Account',
                        f'Click the following link to activate your account: {activation_link}',
                        settings.EMAIL_HOST_USER,
                        [customer.email],
                        fail_silently=False,
                    )
                    return render(request, 'accounts/register_done.html', {"new_user": user_form})
            except Exception as e:
                logger.error(f"Error during registration: {str(e)}")
                user_form.add_error(None, "An error occurred during registration. Please try again.")
        else:
            logger.warning(f"User form errors: {user_form.errors}")
            logger.warning(f"Card form errors: {card_form.errors}")
    else:
        user_form = UserRegistrationForm()
        card_form = CardForm()
    return render(request, 'accounts/register.html', {'user_form': user_form, 'card_form': card_form})

# **Login view**
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                email=cd['email'],
                password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info(f"User {user.email} logged in successfully.")
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
