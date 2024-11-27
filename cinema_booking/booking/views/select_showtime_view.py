# booking/views/select_showtime.py

from . import *

@login_required
def select_showtime(request, movie_id):
    # customer = get_object_or_404(Customer, pk=request.user.pk)
    movie = get_object_or_404(Movie, pk=movie_id)

    # Fetch screenings and theatres
    screenings = Screening.objects.filter(movie=movie).annotate(show_date=Cast('show_time', DateField())).order_by('show_time')
    theatres = Theatre.objects.filter(showroom__screening__movie=movie).distinct()

    # initial_data = { 'selected_month': 0, 'selected_day': 'all'}
    # Instantiate the MonthDayForm
    month_day_form = MonthDayForm()

    # Initialize filter options
    current_date = timezone.now()
    months = [current_date.strftime("%B")]
    months += [(current_date + timedelta(days=30 * i)).strftime("%B") for i in range(1, 3)]
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    if request.method == 'POST':
        month_day_form = MonthDayForm(request.POST)
        if month_day_form.is_valid():
            selected_month = int(month_day_form.cleaned_data['selected_month'])
            selected_day = month_day_form.cleaned_data['selected_day']

            # Apply month filter
            if selected_month == 0:
    # Show all screenings from today onward
                screenings = screenings.filter(show_time__date__gte=current_date.date())
            elif selected_month == 1:
                # Current month, but only from today onward
                screenings = screenings.filter(
                    show_time__month=current_date.month,
                    show_time__date__gte=current_date.date()
                )
            elif selected_month == 2:
                # Next month, all dates
                next_month = (current_date.month % 12) + 1
                screenings = screenings.filter(show_time__month=next_month)
            elif selected_month == 3:
                # Month after next, all dates
                next_month = (current_date.month % 12) + 1
                month_after_next = (next_month % 12) + 1
                screenings = screenings.filter(show_time__month=month_after_next)
            # Apply day filter
            if selected_day != 'all':
                day_index = days_of_week.index(selected_day.capitalize())
                screenings = screenings.filter(show_time__week_day=day_index + 1)

    context = {
        'movie': movie,
        'theatres': theatres,
        'screenings': screenings,
        'months': months,
        'days_of_week': days_of_week,
        'month_day_form': month_day_form,
    }
    return render(request, 'booking/select_showtime.html', context)