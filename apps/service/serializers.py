from rest_framework import serializers

from .models import Service
from ..monitoring.serializers import PeriodicTaskSerializer
from ..notification.models import NotificationChannel


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    periodic_task_data = serializers.JSONField(
        write_only=True, required=False, allow_null=True
    )
    notification_channel = serializers.PrimaryKeyRelatedField(
        queryset=NotificationChannel.objects.all(),
        many=True,
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Service
        fields = (
            "name",
            "description",
            "monitoring_endpoint",
            "is_active",
            "notification_channel",
            "monitoring_type",
            "periodic_task_data",
            "updated_at",
        )

        extra_kwargs = {
            "updated_at": {"read_only": True},
            "notification_channel": {"required": False, "allow_null": True},
        }

    def validate_periodic_task_data(self, value):
        """
        Validate the periodic_task_data to ensure it can create a valid PeriodicTask.
        """
        # Use the PeriodicTaskSerializer or similar logic to validate the incoming data
        serializer = PeriodicTaskSerializer(data=value)
        if not serializer.is_valid():
            raise serializers.ValidationError("Invalid periodic task data.")
        return value

    def create(self, validated_data):
        periodic_task_data = validated_data.pop("periodic_task_data", None)
        notification_channels_data = validated_data.pop("notification_channel", [])

        # Create or link the PeriodicTask here
        if periodic_task_data:
            periodic_task_serializer = PeriodicTaskSerializer(data=periodic_task_data)
            if periodic_task_serializer.is_valid(raise_exception=True):
                periodic_task = periodic_task_serializer.save()
                validated_data["periodic_task"] = periodic_task

        service = Service.objects.create(**validated_data)

        if notification_channels_data:
            service.notification_channel.set(notification_channels_data)

        return service

    def update(self, instance, validated_data):
        # Assuming you may want to update periodic task data as well
        periodic_task_data = validated_data.pop("periodic_task_data", None)

        if periodic_task_data:
            # Update the existing PeriodicTask, if it exists
            periodic_task_serializer = PeriodicTaskSerializer(
                instance.periodic_task, data=periodic_task_data
            )
            if periodic_task_serializer.is_valid(raise_exception=True):
                periodic_task_serializer.save()

        notification_channels_data = validated_data.pop("notification_channel", [])
        if notification_channels_data:
            instance.notification_channel.set(notification_channels_data)

        # Update other fields of Service
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def to_representation(self, instance):
        """
        Modify the output representation to include relevant details of the linked PeriodicTask,
        such as its ID and name.
        """
        representation = super().to_representation(instance)
        if instance.periodic_task:
            representation["periodic_task"] = {
                "id": instance.periodic_task.id,
                "name": getattr(
                    instance.periodic_task, "name", "Unnamed Task"
                ),  # Example field
                "description": getattr(
                    instance.periodic_task, "description", "No description"
                ),  # Example field
            }
        return representation
