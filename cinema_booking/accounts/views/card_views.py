# accounts/views/card_views.py
from . import *
from accounts.services.card_facade import CardFacade

@login_required
def change_payment_method(request):
    user = request.user
    customer = Customer.objects.get(email=user.email)  # Ensure correct customer is fetched
    cards = customer.cards.all()  # Get all cards related to the customer

    facade = CardFacade()

    # Use the CardFacade to decrypt card numbers for display
    for card in cards:
        try:
            card.card_number = facade.decrypt_card_number_safe(card.card_number)  # Decrypt the card number safely
        except Exception:
            messages.error(request, "Failed to decrypt card information. Please contact support.")
            card.card_number = "Invalid"  # Set to Invalid if decryption fails

    if request.method == "POST":
        card_forms = [
            CardForm(request.POST, instance=card, prefix=f'card_{card.pk}', customer=customer)
            for card in cards
        ]
        new_card_form = CardForm(request.POST, prefix='new_card', customer=customer, is_registration=False)

        if all(cf.is_valid() for cf in card_forms) and new_card_form.is_valid():
            try:
                with transaction.atomic():  # Ensure atomic transaction
                    # Update existing cards using the facade
                    for cf in card_forms:
                        card = cf.save(commit=False)
                        card.customer = customer  # Explicitly assign the customer to the card
                        facade.update_card(card, cf.cleaned_data)  # Use facade to encrypt and save the updated card

                    # Add new card if provided
                    if new_card_form.cleaned_data.get('card_number'):
                        new_card = new_card_form.save(commit=False)
                        new_card.customer = customer  # Assign customer to the new card
                        facade.add_card(customer, new_card_form.cleaned_data)  # Use facade to encrypt and save

                    messages.success(request, "Payment methods updated successfully.")
                    return redirect("change_payment_method")
            except Exception as e:
                messages.error(request, f"An error occurred while updating your payment methods: {str(e)}. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Initialize forms for GET requests
        card_forms = [CardForm(instance=card, prefix=f'card_{card.pk}', customer=customer, is_registration=False) for card in cards]
        new_card_form = CardForm(prefix='new_card', customer=customer, is_registration=False)

    context = {
        "card_forms": card_forms,
        "new_card_form": new_card_form,
    }
    return render(request, "accounts/change_payment_method.html", context)




# accounts/views/card_views.py


@login_required
def modify_payment_method(request, card_id=None):
    customer = Customer.objects.get(pk=request.user.pk)
    facade = CardFacade()

    if card_id:
        card = get_object_or_404(customer.cards, id=card_id)
    else:
        card = Card(customer=customer)

    if request.method == "POST":
        form = ModifyCardForm(request.POST, instance=card, customer=customer, is_registration=False)

        if form.is_valid():
            if form.cleaned_data.get('delete'):  # Handle deletion of card
                facade.delete_card(card)  # Call facade to delete card securely
                messages.success(request, "Payment method deleted successfully.")
                return redirect('show_payment_methods')
            else:
                form.save()  # Save updated card details using facade
                facade.update_card(card, form.cleaned_data)  # Encrypt card number and save
                messages.success(request, "Payment method updated successfully.")
                return redirect('show_payment_methods')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Set initial data for the form, including decrypted card data
        initial = {}
        if card_id:
            initial['card_number'] = facade.decrypt_card_number(card.card_number)  # Decrypt card number safely
            initial['card_name'] = card.card_name
            initial['expiry_date'] = card.expiry_date
        form = ModifyCardForm(instance=card, initial=initial, customer=customer)

    return render(request, 'accounts/modify_payment_method.html', {'form': form, 'card': card})



# accounts/views/card_views.py

@login_required
def show_payment_methods(request):
    customer = Customer.objects.get(pk=request.user.pk)
    facade = CardFacade()
    cards = customer.cards.all()

    # Decrypt and mask card number and CVV for display
    for card in cards:
        try:
            card.card_number_safe = facade.decrypt_card_number_safe(card.card_number)  # Decrypt and mask card number
            card.cvv_safe = facade.decrypt_cvv_safe(card.cvv)  # Decrypt and mask CVV
        except Exception:
            messages.error(request, "Failed to decrypt card information. Please contact support.")
            card.card_number_safe = "Invalid"  # Set to Invalid if decryption fails
            card.cvv_safe = "****"  # Mask CVV if decryption fails

    card_count = cards.count()
    disable_add_card = card_count >=4  

    return render(request, 'accounts/show_payment_methods.html', {'cards': cards, 'disable_add_card': disable_add_card})


# accounts/views/card_views.py


@login_required
def delete_payment_method(request, card_id):
    customer = Customer.objects.get(pk=request.user.pk)
    card = get_object_or_404(customer.cards, id=card_id)
    facade = CardFacade()

    # Delete the card securely using the CardFacade
    facade.delete_card(card)
    messages.success(request, "Payment method deleted successfully.")
    return redirect('show_payment_methods')
