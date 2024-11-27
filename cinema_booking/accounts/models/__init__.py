from django.db import models
from django.core.exceptions import ValidationError

from django.db import models
import logging
from cryptography.fernet import Fernet
from django.conf import settings

from .address_models import Address
from .card_models import Card
from .customer_models import Customer
from .card_models import Transaction