from functools import wraps
from django.shortcuts import redirect, render

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        return render(request, '403.html')
    return wrapper

def recruiter_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'recruiter':
            return view_func(request, *args, **kwargs)
        return render(request, '403.html')
    return wrapper

def coordinator_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'coordinator':
            return view_func(request, *args, **kwargs)
        return render(request, '403.html')
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        return render(request, '403.html')
    return wrapper
