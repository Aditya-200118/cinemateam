# admin/admin_views.py

from datetime import datetime, timedelta
from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from accounts.models import Customer, Address, Card
from accounts.forms import UserRegistrationForm, AddressForm, EditProfileForm
from django.urls import reverse_lazy
from accounts.services.user_service import UserService
from accounts.services.email_proxy import EmailProxy, DjangoEmailService
from accounts.services.user_profile_facade import UserProfileFacade
from booking.services.promotion_service import PromotionService
from . import Theatre, Showroom, Movie, Screening, get_object_or_404, JsonResponse, transaction
from .admin_forms import TheatreForm, ShowroomForm, MovieForm, ScreeningForm, PromotionForm, EditMovieForm, MovieTicketTypeDiscountForm
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from booking.models.ticket_model import MovieTicketTypeDiscount, TicketType
from django.urls import reverse
from django.forms import modelformset_factory
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import user_passes_test
class AdminLoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(
            attrs={'placeholder': 'Email address', 'class': 'form-control'}
        )
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}
        )
        self.fields['remember_me'] = forms.BooleanField(
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            label="Remember Me"
        )

class AdminLoginView(auth_views.LoginView):
    template_name = 'admin/login.html'
    authentication_form = AdminLoginForm
    
    def get_success_url(self):
        return reverse_lazy('admin:index')

class AdminLogoutView(auth_views.LogoutView):
    template_name = 'admin/logout.html'

class MyAdminSite(AdminSite):
    site_header = 'Cinema Booking Admin'
    site_title = 'Cinema Booking Admin Portal'
    index_title = 'Welcome to Cinema Booking Admin' 

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
            path('admin-logout/', AdminLogoutView.as_view(), name='admin_logout'),
            path('welcome/', self.admin_view(self.welcome_view), name='admin_welcome'),
            path('accounts/', self.admin_view(self.accounts_view), name='admin_accounts'),
            path('add-customer/', self.admin_view(self.add_customer_view), name='add_customer'),
            path('customer-data/', self.admin_view(self.customer_data), name='customer_data'),
            path('modify-customer/<int:pk>/', self.admin_view(self.modify_customer_view), name='modify_customer'),
            path('delete-customer/<int:pk>/', self.admin_view(self.delete_customer_view), name='delete_customer'),
            
            # Movie scheduling URLs
            path('movie/', self.admin_view(self.movie_admin_home), name='admin_movie'),
            path('add-movie/', self.admin_view(self.add_movie), name='add_movie'),
            path('edit-movie/<int:movie_id>', self.admin_view(self.edit_movie), name='edit_movie'),
            path('movie-data/', self.admin_view(self.movie_data_view), name='movie_data'),
            path('theatre-data/', self.admin_view(self.theatre_data_view), name='theatre_data'),
            path('showroom-schedule/<int:showroom_id>/', self.admin_view(self.showroom_schedule_view), name='showroom_schedule'),
            path('get-showrooms/<int:theatre_id>/', self.admin_view(self.get_showrooms), name='get_showrooms'),

            path('manage_screenings/', self.admin_view(self.manage_screenings), name='manage_screenings'),
            path('get_screenings/<int:movie_id>/<int:theatre_id>/<int:showroom_id>/', self.admin_view(self.get_screenings), name='get_screenings'),
            path('promotion_dashboard/', self.admin_view(self.promotion_dashboard), name="promotion_dashboard"),
            path('promotion_data/', self.admin_view(self.promotion_data), name="promotion_data"),
            path('create_promotion/', self.admin_view(self.create_promotion), name="create_promotions"),
            path('check-promotion-title-code/', self.admin_view(self.check_promotion_title_or_code), name='check_promotion_title'),
        ]
        return custom_urls + urls
    
    def login(self, request, extra_context=None):
        return redirect('admin_login')

    def welcome_view(self, request):
        context = {
            'num_movies': 10,  # Replace with actual query
            'num_users': 150,  # Replace with actual query
            'num_admins': 5,   # Replace with actual query
            'active_promos': 2,  # Replace with actual query
            'screenings_url': reverse_lazy('list_screenings'),  # Link to screenings list
            'add_screening_url': reverse_lazy('add_screening'),  # Link to add screening

        }
        return render(request, 'admin/welcome.html', context)

    def accounts_view(self, request):
        return render(request, 'admin/accounts.html')

    def customer_data(self, request):
        customers = Customer.objects.all()
        return render(request, 'admin/customer_data.html', {'customers': customers})

    # @user_passes_test(lambda user: user.is_superuser)
    def add_customer_view(self, request):
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            address_form = AddressForm(request.POST)
            
            if user_form.is_valid() and address_form.is_valid():
                facade = UserProfileFacade()

                # Extract cleaned data from forms
                address_data = {
                    "billing_address": address_form.cleaned_data["billing_address"],
                    "city": address_form.cleaned_data["city"],
                    "state": address_form.cleaned_data["state"],
                    "zip_code": address_form.cleaned_data["zip_code"],
                }
                profile_data = {
                    "middle_name": user_form.cleaned_data["middle_name"],
                    "contact_no": user_form.cleaned_data["contact_no"],
                    "promotions": user_form.cleaned_data.get("promotions", False),
                }

                try: 
                    with transaction.atomic():
                    # Use the facade to create the customer
                        customer = facade.create_customer(
                            email=user_form.cleaned_data["email"],
                            password=user_form.cleaned_data["password"],
                            first_name=user_form.cleaned_data["first_name"],
                            last_name=user_form.cleaned_data["last_name"],
                            profile_data=profile_data,
                            address_data=address_data,
                        )

                        # Set additional boolean fields from the form
                        customer.is_staff = request.POST.get('is_staff') == 'on'
                        customer.is_superuser = request.POST.get('is_superuser') == 'on'
                        customer.is_active = request.POST.get('is_active') == 'on'
                        customer.save()

                        # Redirect to the admin accounts page after successful customer creation
                        return redirect('admin_accounts')

                except Exception as e:
                    # Log the error and show an error message on the form
                    logger.error(f"Error adding customer: {str(e)}")
                    return render(request, 'admin/add_customer.html', {
                        'user_form': user_form,
                        'address_form': address_form,
                        'error': "Error adding the customer. Please try again."
                    })
        else:
            # Initialize empty forms if the request is not POST
            user_form = UserRegistrationForm()
            address_form = AddressForm()

        # Render the form in the response
        return render(request, 'admin/add_customer.html', {
            'user_form': user_form,
            'address_form': address_form
        })

    # @user_passes_test(lambda user: user.is_superuser)
    def modify_customer_view(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        address = customer.address
        facade = UserProfileFacade()

        if request.method == 'POST':
            user_form = EditProfileForm(request.POST, instance=customer)
            address_form = AddressForm(request.POST, instance=address)

            if user_form.is_valid() and address_form.is_valid():
                profile_data = user_form.cleaned_data
                address_data = address_form.cleaned_data
                try:
                    facade.update_user_profile(customer, profile_data, address_data)

                    # Allow modification of `is_staff`, `is_superuser`, `is_active`
                    customer.is_staff = request.POST.get('is_staff') == 'on'
                    customer.is_superuser = request.POST.get('is_superuser') == 'on'
                    customer.is_active = request.POST.get('is_active') == 'on'
                    customer.save()

                    return redirect('customer_data')
                except Exception as e:
                    return render(request, 'admin/modify_customer.html', {
                        'user_form': user_form, 
                        'address_form': address_form, 
                        'customer': customer, 
                        'error': "Error updating the profile. Please try again later."
                    })
        else:
            user_form = EditProfileForm(instance=customer)
            address_form = AddressForm(instance=address)

        return render(request, 'admin/modify_customer.html', {
            'user_form': user_form, 
            'address_form': address_form, 
            'customer': customer
        })


    def delete_customer_view(self, request, pk):
        try:
            facade = UserProfileFacade()
            customer = Customer.objects.get(user_id=pk)  # Use `user_id` instead of `pk` if needed

            if request.method == "POST":
                facade.delete_customer(request, customer.user_id)  # Call `delete_customer` properly
                return redirect("admin_accounts")
            else:
                return render(request, "admin/customer_data.html", {"customers": Customer.objects.all()})
        except Customer.DoesNotExist:
            # Handle case where customer does not exist
            return render(request, "admin/customer_data.html", {"customers": Customer.objects.all(), "error": "Customer not found."})
        except Exception as e:
            # Handle any other exceptions
            return render(request, "admin/customer_data.html", {"customers": Customer.objects.all(), "error": f"Error deleting the customer: {str(e)}"})
    
    def movie_admin_home(self, request):

        return render(request, 'admin/movie_admin_home.html')

    def theatre_data_view(self, request):
        theatres = Theatre.objects.all()
        return render(request, 'admin/theatre_data.html', {'theatres': theatres})
    
    def movie_data_view(self, request):
        movie = Movie.objects.all()
        return render(request, 'admin/movie_data.html', {'movies': movie})

    def showroom_schedule_view(self, request, showroom_id):
        # Retrieve the showroom by showroom_id
        showroom = get_object_or_404(Showroom, showroom_id=showroom_id)

        # Fetch scheduled movies for this showroom
        screenings = showroom.screening_set.select_related('movie').all()

        sort_by = request.GET.get('sort_by', 'movie_title')

        if sort_by == 'movie_title':
            screenings = screenings.order_by('movie__title')
        elif sort_by == 'show_time':
            screenings = screenings.order_by('show_time')

        return render(request, 'admin/showroom_schedule.html', {
            'showroom': showroom,
            'screenings': screenings,
            'sort_by': sort_by,
        })

    def add_movie(self, request):
        movie_form = MovieForm(request.POST or None, request.FILES or None)

        if request.method == 'POST':
            with transaction.atomic():
                if movie_form.is_valid():
                    # Save the movie object
                    movie = movie_form.save()

                    # Define default discounts for each ticket type
                    default_discounts = {
                        1: 15,  # Ticket type 1
                        2: 30,  # Ticket type 2
                        3: 0,   # Ticket type 3
                    }

                    # Create MovieTicketTypeDiscount objects
                    for ticket_type_id, discount in default_discounts.items():
                        MovieTicketTypeDiscount.objects.create(
                            movie=movie,
                            ticket_type_id=ticket_type_id,
                            discount=discount
                        )

                    return redirect('admin_movie')

        return render(
            request,
            'admin/add_movie.html',
            {
                'movie_form': movie_form,
            }
        )


    def get_showrooms(self, request, theatre_id):
        showrooms = Showroom.objects.filter(theatre_id=theatre_id).values('showroom_id', 'name')
        return JsonResponse({'showrooms': list(showrooms)})
    
    def modify_movie_view(self, request, pk):
        pass

    def modify_theatre_view(self, request, pk):
        pass

    def manage_screenings(self, request):
        # Instantiate the forms
        theatre_form = TheatreForm(request.POST or None)
        showroom_form = ShowroomForm(request.POST or None)
        screening_form = ScreeningForm(request.POST or None)

        # Handle POST request
        if request.method == "POST":
            showroom_id = request.POST.get('showroom_id')
            movie_id = request.POST.get('movie_id')
            show_time = request.POST.get('show_time')

            if not all([showroom_id, movie_id, show_time]):
                messages.error(request, "Missing required fields.")
                return redirect('manage_screenings')  # Redirect to the same page on error

            try:
                # Use the form instance for validation and saving
                showroom = Showroom.objects.get(pk=showroom_id)
                movie = Movie.objects.get(pk=movie_id)
                selected_time = datetime.fromisoformat(show_time)

                # Check for conflicting screenings in the selected showroom
                conflict = Screening.objects.filter(
                    showroom=showroom,
                    show_time__range=[selected_time - timedelta(minutes=15), selected_time + timedelta(minutes=15)]
                ).exists()

                if conflict:
                    messages.error(request, "A conflict exists: There's already a screening scheduled near this time in the selected showroom.")
                    return redirect('manage_screenings')

                # Add the showroom to the form's context so it can be used in validation
                screening_form = ScreeningForm(request.POST, showroom=showroom)
                if screening_form.is_valid():
                    screening = screening_form.save(commit=False)
                    screening.movie = movie  # Set the movie manually
                    screening.showroom = showroom  # Set the showroom manually
                    screening.save()
                    messages.success(request, f"Screening added successfully: {screening}")
                    return redirect('manage_screenings')  # Redirect on success
                else:
                    messages.error(request, "Form is invalid.")
                    return redirect('manage_screenings')

            except Showroom.DoesNotExist:
                messages.error(request, "Showroom does not exist.")
                return redirect('manage_screenings')
            except Movie.DoesNotExist:
                messages.error(request, "Movie does not exist.")
                return redirect('manage_screenings')
            except Exception as e:
                messages.error(request, f"Error: {e}")
                return redirect('manage_screenings')

        # For GET request
        if request.method == "GET":
            movies = Movie.objects.all()
            theatres = Theatre.objects.all()
            showrooms = Showroom.objects.all()
            screenings = Screening.objects.all()
            
            return render(
                request,
                "admin/manage_screenings.html",
                {
                    "theatre_form": theatre_form,
                    "showroom_form": showroom_form,
                    "screening_form": screening_form,
                    "movies": movies,
                    "theatres": theatres,
                    "showrooms": showrooms,
                    "screenings": screenings
                }
            )



    def get_screenings(self, request, movie_id, theatre_id, showroom_id):
        try:
            screenings = Screening.objects.filter(
                movie_id=movie_id, showroom__theatre_id=theatre_id, showroom_id=showroom_id
            ).select_related("showroom", "showroom__theatre")

            data = [
                {
                    "id": screening.screening_id,
                    "theatre": screening.showroom.theatre.name,
                    "showroom": screening.showroom.name,
                    "show_time": screening.show_time.isoformat(),
                }
                for screening in screenings
            ]
            return JsonResponse({"screenings": data})
        except Exception as e:
            logger.error(f"Error fetching screenings for movie_id={movie_id}: {e}")
            return JsonResponse({"error": "Error fetching screenings"}, status=500)

    def promotion_dashboard(self, request):
        # This view only renders the navigation page for promotion management.
        return render(request, 'admin/promotion_dashboard.html')

    def promotion_data(self, request):
        # Fetch active and future promotions for display
        active_promotions = PromotionService.get_active_promotions()
        future_promotions = PromotionService.get_future_promotions()

        return render(request, 'admin/promotion_data.html', {
            'active_promotions': active_promotions,
            'future_promotions': future_promotions
        })

    def create_promotion(self, request):
        user_service = UserService()
        email_proxy = EmailProxy(DjangoEmailService())

        if request.method == 'POST':
            form = PromotionForm(request.POST)
            if form.is_valid():
                # Create the promotion using the service
                promotion_data = form.cleaned_data
                try:
                    PromotionService.create_promotion(
                        promo_code=promotion_data['promo_code'],
                        title=promotion_data['title'],
                        description=promotion_data['description'],
                        discount=promotion_data['discount'],
                        valid_from=promotion_data['valid_from'],
                        valid_to=promotion_data['valid_to']
                    )

                    # Get users signed up for promotions
                    users = user_service.get_users_signed_up_for_promotions()

                    # Send email to these users, now uses proxy
                    subject = f"New Promotion: {promotion_data['title']}"
                    message = (
                        f"Dear Customer,\n\n"
                        f"We're excited to announce a new promotion:\n\n"
                        f"Title: {promotion_data['title']}\n"
                        f"Description: {promotion_data['description']}\n"
                        f"Discount: {promotion_data['discount']}%\n"
                        f"Valid From: {promotion_data['valid_from']}\n"
                        f"Valid To: {promotion_data['valid_to']}\n\n"
                        f"Don't miss out!"
                    )
                    recipient_list = [user.email for user in users]

                    email_proxy.send_email(subject, message, recipient_list)

                    messages.success(request, "Promotion created and emails sent successfully!")
                    return redirect('admin:create_promotion')
                except Exception as e:
                    messages.error(request, f"Failed to create promotion or send emails: {e}")
            else:
                messages.error(request, "Invalid form submission. Please correct the errors.")
        else:
            form = PromotionForm()

        return render(request, 'admin/create_promotion.html', {
            'form': form
        })


    def check_promotion_title_or_code(self, request):
        title = request.GET.get("title", "").strip()
        promo_code = request.GET.get("promo_code", "").strip()
        if not title and not promo_code:
            return JsonResponse({"error": "Either title or promo code is required."}, status=400)
        try:
            exists = PromotionService.promotion_exists_by_title_or_code(title, promo_code)
            return JsonResponse({"exists": exists})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

    def edit_movie(self, request, movie_id):
        # Fetch the movie instance
        movie = get_object_or_404(Movie, movie_id=movie_id)

        # Initialize movie form
        movie_form = EditMovieForm(instance=movie)

        # Fetch the discount data for the movie
        discounts = MovieTicketTypeDiscount.objects.filter(movie=movie)
        initial_data = {
            'child_discount': discounts.filter(ticket_type__type='Child').first().discount if discounts.filter(ticket_type__type='Child').exists() else 0,
            'adult_discount': discounts.filter(ticket_type__type='Adult').first().discount if discounts.filter(ticket_type__type='Adult').exists() else 0,
            'senior_discount': discounts.filter(ticket_type__type='Senior').first().discount if discounts.filter(ticket_type__type='Senior').exists() else 0,
        }

        # Initialize discount form with initial data
        discount_form = MovieTicketTypeDiscountForm(initial=initial_data)

        if request.method == 'POST':
            movie_form = EditMovieForm(request.POST, request.FILES, instance=movie)
            discount_form = MovieTicketTypeDiscountForm(request.POST)

            if movie_form.is_valid() and discount_form.is_valid():
                with transaction.atomic():
                    # Save the movie
                    movie = movie_form.save()

                    # Save the discounts
                    MovieTicketTypeDiscount.objects.update_or_create(
                        movie=movie, 
                        ticket_type=TicketType.objects.get(type='Child'), 
                        defaults={'discount': discount_form.cleaned_data['child_discount']}
                    )
                    MovieTicketTypeDiscount.objects.update_or_create(
                        movie=movie, 
                        ticket_type=TicketType.objects.get(type='Adult'), 
                        defaults={'discount': discount_form.cleaned_data['adult_discount']}
                    )
                    MovieTicketTypeDiscount.objects.update_or_create(
                        movie=movie, 
                        ticket_type=TicketType.objects.get(type='Senior'), 
                        defaults={'discount': discount_form.cleaned_data['senior_discount']}
                    )

                    return redirect('movie_data')  # Redirect to the movie list or another page

        return render(
            request,
            'admin/edit_movie.html',
            {
                'movie_form': movie_form,
                'discount_form': discount_form
            }
        )

admin_site = MyAdminSite(name='myadmin')