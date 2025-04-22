from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from recommendation.decorators import admin_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from recommendation.models import *
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.db.models import Sum

User = get_user_model()

@admin_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('user_panel')

    total_products = HandicraftProduct.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.filter(role='USER').count()
    total_orders = Order.objects.count()
    total_items_sold = Order.objects.filter(status='CONFIRMED').aggregate(total=Sum('quantity'))['total'] or 0

    return render(request, 'recommendation/admin/dashboard.html', {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_items_sold': total_items_sold,
    })

@admin_required
def admin_questions_view(request):
    questions = Question.objects.all().order_by('-created_at')  # You can filter unanswered if you want

    return render(request, 'recommendation/admin/questions.html', {
        'questions': questions
    })

@admin_required
def admin_answer_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        answer_text = request.POST.get('answer')
        if answer_text:
            # Create the answer
            answer = Answer.objects.create(
                question=question,
                responder=request.user,
                content=answer_text
            )

            # Update question status
            question.status = 'ANSWERED'
            question.save()

    return redirect('admin_questions')


def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')

def admin_root_redirect(request):
    if request.user.is_authenticated and request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    return redirect('admin_login')


@admin_required
def admin_orders_view(request):
    orders = Order.objects.select_related('product', 'user').filter(status='PENDING').order_by('-order_date')
    return render(request, 'recommendation/admin/orders.html', {
        'orders': orders
    })


@admin_required
@require_POST
def confirm_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'CONFIRMED'
    order.save()
    return redirect('admin_orders')