from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from recommendation.models import HandicraftProduct 
import random
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash


User = get_user_model()


def home_view(request):
    all_products = list(HandicraftProduct.objects.all())
    random.shuffle(all_products)

    trending_products = all_products[:10]
    more_products = all_products[5:15]

    return render(request, 'recommendation/user/home.html', {
        'trending_products': trending_products,
        'more_products': more_products,
    })

@login_required
def profile_view(request):
    return render(request, 'recommendation/user/profile.html')

@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        if not full_name or not email:
            messages.error(request, "Name and email are required.")
        elif User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "Email already taken.")
        else:
            user.full_name = full_name
            user.contact = contact
            user.email = email
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_profile')

    return render(request, 'recommendation/user/edit_profile.html', {'user': user})


@login_required
def change_password_view(request):
    user = request.user

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        elif not new_password:
            messages.error(request, "New password cannot be empty.")
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Prevent logout
            messages.success(request, "Password changed successfully.")
            return redirect('user_profile')

    return render(request, 'recommendation/user/change_password.html')