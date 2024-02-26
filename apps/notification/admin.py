from django.contrib import admin
from .models import NotificationChannel, NotificationLog

admin.site.register(NotificationChannel)
admin.site.register(NotificationLog)
