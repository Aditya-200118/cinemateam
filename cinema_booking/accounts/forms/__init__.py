from django import forms
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .address_forms import AddressForm
from .card_forms import CardForm, ModifyCardForm
from .customer_auth_forms import UserRegistrationForm, LoginForm
from .edit_profile_forms import EditProfileForm
from .change_password_forms import CustomPasswordChangeForm, PasswordResetRequestForm
from django.core.exceptions import ValidationError
import re