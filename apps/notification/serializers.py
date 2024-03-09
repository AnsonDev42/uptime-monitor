from pydantic_core import ValidationError
from rest_framework import serializers

from apps.notification.models import NotificationChannel, NotificationType
from apps.notification.notify_services.bark import Bark
from apps.notification.notify_services.telegram import Telegram


class NotificationChannelSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.ChoiceField(choices=NotificationType.choices)
    url = serializers.URLField(required=False)

    class Meta:
        model = NotificationChannel
        fields = (
            "id",
            "name",
            "details",
            "type",
            "url",
        )  # Explicitly include 'id' and other fields you need

    def validate(self, attrs):
        details = attrs.get("details")
        channel_type = attrs.get("type")
        match channel_type:
            case NotificationType.TELEGRAM:
                pydantic_model = Telegram
            case NotificationType.BARK:
                pydantic_model = Bark
            case _:
                pydantic_model = None

        if pydantic_model:
            try:
                # Validates the details using the Pydantic model
                pydantic_model(**details)
            except ValidationError as e:
                raise serializers.ValidationError({"details": e.errors()})

        return attrs

    def create(self, validated_data):
        channel = NotificationChannel.objects.create(**validated_data)
        return channel

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.details = validated_data.get("details", instance.details)
        instance.type = validated_data.get("type", instance.type)
        instance.save()
        return instance
