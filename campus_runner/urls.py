"""
URL configuration for campus_runner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# campus_runner/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt  # ✅ Import added

@csrf_exempt
def create_superuser(request):
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='245122750306',
            email='245122750306@mvsrec.edu.in',
            password='Jbunny@123'
        )
        return HttpResponse("✅ Superuser '245122750306' created with password 'Jbunny@123'.")
    return HttpResponse("⚠️ Superuser already exists.")

@csrf_exempt
def run_migrations(request):
    call_command('migrate')
    return HttpResponse("✅ Migrations completed successfully!")

@csrf_exempt
def run_collectstatic(request):
    call_command('collectstatic', interactive=False)
    return HttpResponse("✅ Static files collected.")

urlpatterns = [
    path('create-admin/', create_superuser),
    path('run-migrations/', run_migrations),
    path('collectstatic/', run_collectstatic),  # Temporary setup URLs
    path('', include('accounts.urls')),
    path('student/', include('student.urls')),
    path('company/', include('companies.urls')),
    path('coordinator/', include('coordinator.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
