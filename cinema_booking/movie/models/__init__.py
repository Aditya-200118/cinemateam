# movie/models/__init__.py

from django.apps import apps 
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

"""Importing all the Models"""
from .theatre_models import Theatre
from .showroom_models import Showroom
from .movie_models import Movie
from .screening_models import Screening