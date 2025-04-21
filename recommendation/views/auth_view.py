from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..forms import UserRegistrationForm, UserLoginForm
from ..models import User

# USER LOGIN VIEW
def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user and user.role == 'USER':
                login(request, user)
                return redirect('user_panel')
            form.add_error(None, "Invalid credentials or not a user account.")
    else:
        form = UserLoginForm()
    return render(request, 'recommendation/user/login.html', {'form': form})


def admin_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user and user.role == 'ADMIN':
                login(request, user)  # 🔐 logs the admin in
                return redirect('admin_dashboard')  # 🔁 sends to admin dashboard
            form.add_error(None, "Invalid credentials or not an admin.")
    else:
        form = UserLoginForm()
    
    return render(request, 'recommendation/admin/login.html', {'form': form})


# REGISTER USER
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('user_login')  # user login
    else:
        form = UserRegistrationForm()
    return render(request, 'recommendation/user/register.html', {'form': form})


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('user_login')
