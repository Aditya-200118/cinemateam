# movie/admin_views2.py
# from . import *

# def list_screenings_view(request):
#     screenings = Screening.objects.select_related('movie', 'showroom').all()
#     return render(request, 'admin/list_screenings.html', {'screenings': screenings})

# def add_screening_view(request):
#     if request.method == 'POST':
#         form = ScreeningForm(request.POST)
#         if form.is_valid():
#             try:
#                 movie = form.cleaned_data['movie']
#                 showroom = form.cleaned_data['showroom']
#                 show_time = form.cleaned_data['show_time']
#                 Screening.schedule_screening(movie, showroom, show_time)  # Use model method with conflict check
#                 messages.success(request, "Screening scheduled successfully.")
#                 return redirect('list_screenings')
#             except ValidationError as e:
#                 messages.error(request, f"Scheduling conflict: {e}")
#     else:
#         form = ScreeningForm()
#     return render(request, 'admin/add_screening.html', {'form': form})

# def delete_screening_view(request, pk):
#     screening = get_object_or_404(Screening, pk=pk)
#     if request.method == 'POST':
#         screening.delete()
#         messages.success(request, "Screening deleted successfully.")
#         return redirect('list_screenings')
#     return render(request, 'admin/confirm_delete_screening.html', {'screening': screening})


# # movie/forms.py

# from django import forms
# # from .models import Screening, Movie, Showroom

# class ScreeningForm(forms.ModelForm):
#     class Meta:
#         model = Screening
#         fields = ['movie', 'showroom', 'show_time']
#         widgets = {
#             'show_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }
# # movie/forms.py

# # from django import forms
# # from .models import Screening, Movie, Showroom

# class ScreeningForm(forms.ModelForm):
#     class Meta:
#         model = Screening
#         fields = ['movie', 'showroom', 'show_time']
#         widgets = {
#             'show_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }