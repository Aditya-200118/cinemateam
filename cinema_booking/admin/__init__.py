# admin/__init__.py

from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import Address, Customer, Card
from movie.models import Movie, Screening, Showroom, Theatre
from booking.models import Booking, Promotion, Ticket, Ticket, TicketType, MovieTicketTypeDiscount
from django import forms