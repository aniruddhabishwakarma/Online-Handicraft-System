from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from recommendation.models import HandicraftProduct 
import random



def home_view(request):
    all_products = list(HandicraftProduct.objects.all())
    random.shuffle(all_products)

    trending_products = all_products[:10]
    more_products = all_products[5:15]

    return render(request, 'recommendation/user/home.html', {
        'trending_products': trending_products,
        'more_products': more_products,
    })