from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from recommendation.models import HandicraftProduct, Category, Cart, Order
import random
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.urls import reverse
from recommendation.utils.recommendation_utils import get_collaborative_recommendations



User = get_user_model()


def home_view(request):
    all_products = list(HandicraftProduct.objects.all())
    random.shuffle(all_products)

    trending_products = all_products[:10]
    more_products = all_products[5:15]
    categories = Category.objects.annotate(product_count=Count('products'))

    # Random category with at least 1 product
    category_with_products = [cat for cat in categories if cat.products.exists()]
    random_category = random.choice(category_with_products) if category_with_products else None
    random_category_products = random_category.products.all()[:10] if random_category else []

    recommended_products = []
    if request.user.is_authenticated:
        recommended_products = get_collaborative_recommendations(request.user.id)


    return render(request, 'recommendation/user/home.html', {
        'trending_products': trending_products,
        'more_products': more_products,
        'categories': categories,
        'random_category': random_category,
        'random_category_products': random_category_products,
        'recommended_products': recommended_products,
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

@login_required
def place_order_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(HandicraftProduct, id=product_id)

        try:
            quantity = int(request.POST.get('quantity') or 1)
        except ValueError:
            quantity = 1  # fallback in case of bad data

        # Prevent invalid or zero quantity
        if quantity <= 0:
            quantity = 1

        # Check stock and place order
        if product.quantity_available >= quantity:
            Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity
            )
            product.quantity_available -= quantity
            product.save()

            # ✅ Redirect to My Orders page after order
            return redirect('my_orders')

        # If out of stock, go back to product page (optional: show message)
        return redirect(reverse('product_detail', kwargs={'id': product.id}))
    
@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).select_related('product').order_by('-order_date')
    return render(request, 'recommendation/user/my_orders.html', {
        'orders': orders
    })
