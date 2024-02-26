from rest_framework import serializers

from apps.notification.models import NotificationChannel, NotificationType


class NotificationChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NotificationChannel
        fields = "__all__"
        type = serializers.ChoiceField(choices=NotificationType.choices)
