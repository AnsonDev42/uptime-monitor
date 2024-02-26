from django.contrib import admin
from .models import NotificationChannel, NotificationLog


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "details")
    search_fields = ("name", "type", "details")


admin.site.register(NotificationLog)
