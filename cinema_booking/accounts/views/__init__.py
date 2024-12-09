# accounts/views/__init__.py

# Common imports used across multiple views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from django.forms import model_to_dict
from django.views import View
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash

from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import logging

from accounts.forms import (
    LoginForm,
    UserRegistrationForm,
    AddressForm,
    EditProfileForm,
    PasswordResetRequestForm,
    CardForm,
    ModifyCardForm
)

from accounts.models import Customer, Card, Address

from accounts.services.user_profile_facade import UserProfileFacade
