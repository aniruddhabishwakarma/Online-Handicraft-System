from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from recommendation.decorators import admin_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from recommendation.models import *
from django.contrib.auth import get_user_model


User = get_user_model()

@admin_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('user_panel')

    total_products = HandicraftProduct.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.filter(role='USER').count()
    

    return render(request, 'recommendation/admin/dashboard.html', {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_users': total_users,
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