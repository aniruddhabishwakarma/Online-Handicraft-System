from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    @wraps(view_func)
    @login_required(login_url='admin_login')
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            return HttpResponseForbidden("Access Denied: Not an admin.")
        return view_func(request, *args, **kwargs)
    return wrapper