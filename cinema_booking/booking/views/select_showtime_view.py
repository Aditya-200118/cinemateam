# booking/views/select_showtime.py

from . import *
from pytz import timezone as pytz_timezone  # 
from datetime import datetime
# booking/views/select_showtime.py

@login_required
def select_showtime(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    current_date = timezone.now()
    # Fetch screenings and theatres
    screenings = (
        Screening.objects.filter(
            movie=movie, show_time__date__gte=current_date.date()
        )
        .annotate(show_date=Cast("show_time", DateField()))
        .order_by("show_time")
    )
    theatres = Theatre.objects.filter(showroom__screening__movie=movie).distinct()

    # Set up form with default values for GET requests
    if request.method == "POST":
        month_day_form = MonthDayForm(request.POST)  # Handle form data on POST
        if month_day_form.is_valid():
            selected_month = int(month_day_form.cleaned_data["selected_month"])
            selected_day = month_day_form.cleaned_data["selected_day"]

            # Apply month filter
            if selected_month == 0:
                # Show all screenings from today onward
                screenings = screenings.filter(show_time__date__gte=current_date.date())
            elif selected_month == 1:
                # Current month only from today onward
                screenings = screenings.filter(
                    show_time__month=current_date.month,
                    show_time__date__gte=current_date.date(),
                )
            elif selected_month == 2:
                # Next month, all dates
                next_month = (current_date.month % 12) + 1
                screenings = screenings.filter(
                    show_time__month=next_month,
                    show_time__date__gte=current_date.date(),
                )
            elif selected_month == 3:
                # Month after next
                next_month = (current_date.month % 12) + 1
                month_after_next = (next_month % 12) + 1
                screenings = screenings.filter(
                    show_time__month=month_after_next,
                    show_time__date__gte=current_date.date(),
                )

            # **Apply the weekday filter independently**
            if selected_day != "all":
                days_of_week = [
                    "Sunday",
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                ]
                day_index = days_of_week.index(selected_day.capitalize())
                screenings = screenings.filter(
                    show_time__week_day=day_index + 1,
                    show_time__date__gte=current_date.date(),
                )
    else:
        # Handle GET request with default initial values
        month_day_form = MonthDayForm(initial={"selected_month": 0, "selected_day": "all"})

    selected_day = month_day_form['selected_day'].value()
    if selected_day and selected_day != "all":
        days_of_week = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        day_index = days_of_week.index(selected_day.capitalize())
        screenings = screenings.filter(
            show_time__week_day=day_index + 1,
            show_time__date__gte=current_date.date(),
        )

    context = {
        "movie": movie,
        "theatres": theatres,
        "screenings": screenings,
        "month_day_form": month_day_form,
    }
    return render(request, "booking/select_showtime.html", context)

