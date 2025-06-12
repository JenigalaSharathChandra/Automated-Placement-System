# accounts/urls.py

from django.urls import path
from .views import home, home_redirect, login_view, register_view, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('home/', home_redirect, name='home_redirect'),

    # Authentication
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
