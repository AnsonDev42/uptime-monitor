# Create your views here.
from rest_framework import viewsets
from .models import NotificationChannel
from .serializers import NotificationChannelSerializer
from django.views.decorators.csrf import csrf_exempt


class NotificationChannelViewSet(viewsets.ModelViewSet):
    queryset = NotificationChannel.objects.all().order_by("name")
    serializer_class = NotificationChannelSerializer

    # permission_classes = [permissions.IsAuthenticated]
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class NotificationChannelGroupViewSet(viewsets.ModelViewSet):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# @csrf_exempt
# dj_rest_auth.views.LoginView()
