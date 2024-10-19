from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import Customer, Card
from .forms import (
    LoginForm,
    UserRegistrationForm,
    CardForm
)

from django.db import transaction
import logging

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
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        card_form = CardForm(request.POST)
        if user_form.is_valid() and card_form.is_valid():
            email = user_form.cleaned_data['email']
            if get_user_model().objects.filter(email=email).exists():
                user_form.add_error('email', 'Email already in use.')
                logger.warning("Email already in use: %s", email)
            else:
                try:
                    with transaction.atomic(): # using atomic transactions as creating customer for failing
                        # Creating the Customer instance directly (need to check multilayer arch design)
                        customer = Customer(
                            first_name=user_form.cleaned_data['first_name'],
                            middle_name=user_form.cleaned_data['middle_name'],
                            last_name=user_form.cleaned_data['last_name'],
                            contact_no=user_form.cleaned_data['contact_no'],
                            email=user_form.cleaned_data['email'],
                            billing_address=user_form.cleaned_data['billing_address'],
                            city=user_form.cleaned_data['city'],
                            state=user_form.cleaned_data['state'],
                            zip_code=user_form.cleaned_data['zip_code']
                        )
                        customer.set_password(user_form.cleaned_data['password'])
                        customer.save()
                        logger.info("New customer created: %s", customer.email)
                        
                        # Create Card instance
                        Card.objects.create(customer=customer, **card_form.cleaned_data)
                        logger.info("Customer and card created successfully.")
                        return render(request, 'accounts/register_done.html', {"new_user":user_form})  # Render a success page. Will change to redirect later once things are fixed
                except Exception as e:
                    logger.error("Error during registration: %s", str(e))
                    user_form.add_error(None, "An error occurred during registration. Please try again.")
        else:
            logger.warning("User form errors: %s", user_form.errors)
            logger.warning("Card form errors: %s", card_form.errors)
    else:
        user_form = UserRegistrationForm()
        card_form = CardForm()
    return render(request, 'accounts/register.html', {'user_form': user_form, 'card_form': card_form})