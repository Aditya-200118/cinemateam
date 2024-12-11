from . import *
from accounts.forms import CardForm
from django.contrib.messages import get_messages

@login_required
def profile_view(request):
    user = get_object_or_404(Customer, pk=request.user.pk)
    address_form = AddressForm(instance=user.address)
    card_form = CardForm()

    context = {
        'user': user,
        'address_form': address_form,
        'card_form': card_form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    customer = Customer.objects.get(email=user.email)
    facade = UserProfileFacade()  # creating a facade object or initialzing the facade

    if request.method == "POST":
        profile_form = EditProfileForm(request.POST, instance=customer)
        address_form = AddressForm(request.POST, instance=customer.address)

        if profile_form.is_valid() and address_form.is_valid():
            profile_data = profile_form.cleaned_data
            address_data = address_form.cleaned_data

            try:
                facade.update_user_profile(customer, profile_data, address_data)
                messages.add_message(request, messages.SUCCESS, "Your profile has been updated successfully.", extra_tags='profile_update')
                # storage = get_messages(request)  # Consumes all messages
                # for _ in storage:  # Clears them explicitly
                #     pass
                return redirect("profile")
            except Exception:
                messages.error(request, "An error occurred while updating your profile. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        profile_form = EditProfileForm(instance=customer)
        address_form = AddressForm(instance=customer.address)

    context = {
        "profile_form": profile_form,
        "address_form": address_form,
    }
    return render(request, "accounts/edit_profile.html", context)