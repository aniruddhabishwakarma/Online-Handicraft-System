from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..forms import UserRegistrationForm, UserLoginForm
from ..models import User
from django.contrib import messages

def user_login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Both fields are required.")
        else:
            user = authenticate(email=email, password=password)
            if user and user.role == 'USER':
                login(request, user)
                return redirect(next_url)
            else:
                messages.error(request, "Invalid credentials or not a user account.")

    return render(request, 'recommendation/user/login.html', {'next': next_url})

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


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 🔒 Basic validations
        if not all([email, username, full_name, contact, password, confirm_password]):
            messages.error(request, "All fields are required.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            # ✅ Create user
            user = User.objects.create_user(
                email=email,
                username=username,
                full_name=full_name,
                contact=contact,
                password=password,
                role='USER'
            )
            messages.success(request, "Account created successfully. Please login.")
            return redirect('user_login')  # ✅ Success redirect

    # 🟡 Always render template for both GET and failed POST
    return render(request, 'recommendation/user/register.html')
    

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('user_login')
