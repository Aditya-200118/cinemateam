from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from accounts.models import Customer
from accounts.forms import CardForm
from booking.models import (
    Booking, 
    Ticket, 
    Promotion, 
    TicketType, 
    MovieTicketTypeDiscount
)
from booking.forms import BookingForm, PromotionForm, TicketTypeForm, MonthDayForm
from movie.models import Movie, Screening, Theatre
from django.db.models import DateField
from datetime import timedelta
from django.db.models.functions import Cast
from math import ceil
import json
from django.http import JsonResponse

from django.core.exceptions import ValidationError