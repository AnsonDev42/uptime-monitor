"""
URL configuration for uptimemonitor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apps.notification.views import NotificationChannelViewSet
from apps.service.views import ServiceViewSet
from apps.monitoring.views import (
    IntervalScheduleViewSet,
    PeriodicTaskViewSet,
    UptimeRecordViewSet,
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"notify", NotificationChannelViewSet)
router.register(r"service", ServiceViewSet)
router.register(r"beat", IntervalScheduleViewSet)
router.register(r"task", PeriodicTaskViewSet)
router.register(r"uptime", UptimeRecordViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls"), name="rest_framework"),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
]

urlpatterns += router.urls
