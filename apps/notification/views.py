# Create your views here.
from rest_framework import viewsets, permissions
from .models import NotificationChannel
from .serializers import NotificationChannelSerializer


class NotificationChannelViewSet(viewsets.ModelViewSet):
    queryset = NotificationChannel.objects.all().order_by("name")
    serializer_class = NotificationChannelSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationChannelGroupViewSet(viewsets.ModelViewSet):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    permission_classes = [permissions.IsAuthenticated]
