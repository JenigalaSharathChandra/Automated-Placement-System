from django.contrib import admin
from .models import User, Student, PlacementCoordinator, ActivityLog

admin.site.register(User)
admin.site.register(Student)
admin.site.register(PlacementCoordinator)
admin.site.register(ActivityLog)