from rest_framework import serializers

from apps.notification.models import NotificationChannel, NotificationType


class NotificationChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NotificationChannel
        fields = (
            "id",
            "name",
            "details",
            "type",
            "url",
        )  # Explicitly include 'id' and other fields you need
        type = serializers.ChoiceField(choices=NotificationType.choices)
