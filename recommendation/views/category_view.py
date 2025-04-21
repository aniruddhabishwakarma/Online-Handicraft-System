from django.shortcuts import render, get_object_or_404, redirect
from recommendation.models import Category
from recommendation.forms import CategoryForm
from recommendation.decorators import admin_required
from django.contrib import messages

@admin_required
def category_list(request):
    show_modal = False
    selected_category = None
    products = []

    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('admin_categories')

    # When clicking a category card
    category_id = request.GET.get('category')
    if category_id:
        selected_category = Category.objects.get(id=category_id)
        products = selected_category.products.all()
        show_modal = True

    categories = Category.objects.all()
    return render(request, 'recommendation/admin/categories.html', {
        'categories': categories,
        'show_modal': show_modal,
        'selected_category': selected_category,
        'products': products
    })


@admin_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect('admin_categories')
    else:
        form = CategoryForm()
    return render(request, 'recommendation/admin/category_form.html', {'form': form, 'title': 'Add Category'})

@admin_required
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'recommendation/admin/category_form.html', {'form': form, 'title': 'Edit Category'})

@admin_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect('admin_categories')