from django.shortcuts import render, redirect, get_object_or_404
from recommendation.models import HandicraftProduct, Category, Question
from recommendation.decorators import admin_required
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from recommendation.utils.recommendation_utils import *

@admin_required
def list_products(request):
    products = HandicraftProduct.objects.all().order_by('-id')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'recommendation/admin/products.html', {
        'page_obj': page_obj,
        'categories': categories
    })

@admin_required
def add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        category = get_object_or_404(Category, id=request.POST['category'])

        HandicraftProduct.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            currency=request.POST.get('currency', 'USD'),
            description=request.POST['description'],
            image_file=request.FILES.get('image_file'),  # ✅ handle upload
            quantity_available=request.POST['quantity_available'],
            category=category
        )
        return redirect('admin_products')

    return render(request, 'recommendation/admin/add_product.html', {
        'categories': categories
    })

@admin_required
def edit_product(request, pk):
    product = get_object_or_404(HandicraftProduct, pk=pk)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.currency = request.POST.get('currency', 'NPR')
        product.description = request.POST['description']
        product.quantity_available = request.POST['quantity_available']
        product.category = get_object_or_404(Category, id=request.POST['category'])

        if request.FILES.get('image_file'):
            product.image_file = request.FILES['image_file']

        product.save()
        return redirect('admin_products')  # ✅ redirect back to product list

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'recommendation/admin/edit_product_modal.html', {
            'product': product,
            'categories': categories
        })

    return render(request, 'recommendation/admin/edit_product.html', {
        'product': product,
        'categories': categories
    })


@admin_required
def delete_product(request, pk):
    product = get_object_or_404(HandicraftProduct, pk=pk)
    product.delete()
    return redirect('admin_products')


def product_detail_view(request, id):
    product = get_object_or_404(HandicraftProduct, id=id)
    questions = Question.objects.filter(product=product).order_by('-created_at')
    ordered = request.GET.get("ordered") == "true"

    similar_products = get_similar_products(product)
    return render(request, 'recommendation/user/product_detail.html', {
        'product': product,
        'questions': questions,
        'ordered': ordered, 
        'similar_products': similar_products,
        })

def search_products_view(request):
    query = request.GET.get('q', '')
    products = HandicraftProduct.objects.filter(name__icontains=query)[:5]

    results = [{
        'id': p.id,
        'name': p.name,
        'image_url': p.image_file.url if p.image_file else '/static/images/default.png'
    } for p in products]

    return JsonResponse(results, safe=False)

@login_required
def add_question_view(request, product_id):
    product = get_object_or_404(HandicraftProduct, id=product_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Question.objects.create(
                product=product,
                user=request.user,
                content=content,
                status='UNANSWERED'
            )
        # Redirect back to the same product page after posting
        return redirect('product_detail', id=product.id)

    # In case someone visits directly (not typical), redirect to product page
    return redirect('product_detail', product_id=product.id)


def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = HandicraftProduct.objects.filter(category=category)

    return render(request, 'recommendation/user/category_products.html', {
        'category': category,
        'products': products,
    })


