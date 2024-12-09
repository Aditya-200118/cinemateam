from . import *
User = get_user_model()
from accounts.forms import CustomPasswordChangeForm
from accounts.services.email_proxy import EmailProxy, DjangoEmailService

# mvc ~ mvt(django)

# model = model
# view = templates
# controller = views (presentation_layer + controller + business logic)


logger = logging.getLogger(__name__)
def generate_temp_password(length=12):
    #random temparary passowrd
    return get_random_string(length)

from django.contrib.auth import get_user_model

def password_reset_request(request):
    
    email_service = EmailProxy(DjangoEmailService())  # Use the Proxy
    
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST) # changes passwordresetrequest to custom
        if form.is_valid():
            email = form.cleaned_data['email']
            try:

                user_model = get_user_model()
                user = user_model.objects.get(email=email)

                temp_password = generate_temp_password()
                hashed_password = make_password(temp_password)

                user.password = hashed_password
                user.save()
                subject = 'Temporary Password for Your Account'
                message = (
                    f'Hello {user.first_name},\n\n'
                    f'Your temporary password is: {temp_password}\n'
                    'Please log in and change your password immediately.\n\n'
                    'Thank you!'
                )
                try:
                    email_service.send_email(subject, message, [email])
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")

                return redirect('password_reset_done')

            except user_model.DoesNotExist: 
                form.add_error('email', 'No user with this email address exists.')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'registration/password_reset_form.html', {'form': form})


def password_reset_confirm(request, token):
    try:
        user = User.objects.get(reset_token=token)
    except User.DoesNotExist:
        return redirect("password_reset_invalid")

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            user.reset_token = ""
            user.save()
            return redirect("password_reset_complete")
    else:
        form = SetPasswordForm(user)
    return render(request, "registration/password_reset_confirm.html", {"form": form})


def password_reset_done(request):
    return render(request, "registration/password_reset_done.html")


def password_reset_complete(request):
    return render(request, "registration/password_reset_complete.html")


@login_required
def change_password_view(request):
    email_service = EmailProxy(DjangoEmailService())  
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            
            # Send email notification
            subject = 'Password Changed Successfully'
            message = (
                f"Hello {request.user.first_name},\n\n"
                f"Your password has been changed successfully.\n"
                "If you did not make this change, please contact support immediately.\n\n"
                "Thank you."
            )
            try:
                email_service.send_email(subject, message, [request.user.email])
                logger.info(f"Password change email sent to {request.user.email}")
            except Exception as e:
                logger.error(f"Failed to send password change email: {str(e)}")

            
            return redirect('home')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})