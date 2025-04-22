from django.shortcuts import render, redirect, get_object_or_404
from recommendation.models import HandicraftProduct, Category
from recommendation.decorators import admin_required
from django.core.paginator import Paginator

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
    return render(request, 'recommendation/user/product_detail.html', {'product': product})



