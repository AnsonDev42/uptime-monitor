from rest_framework import serializers
from rest_framework.utils import json

from apps.service.models import Service
from apps.monitoring.serializers import (
    PeriodicTaskSerializer,
    IntervalScheduleSerializer,
)
from apps.notification.models import NotificationChannel


def create_periodic_task(task_data):
    # Assuming 'IntervalScheduleSerializer' and related models are properly imported
    # Deserialize the task data to create a new PeriodicTask

    if "interval" in task_data and isinstance(task_data["interval"], dict):
        interval_data = task_data.pop("interval")
        interval_serializer = IntervalScheduleSerializer(data=interval_data)
        if interval_serializer.is_valid(raise_exception=True):
            interval = interval_serializer.save()
        else:
            raise ValueError("Invalid 'interval' data for PeriodicTask creation.")
    else:
        # Handle cases where 'interval' data might be missing or invalid
        raise ValueError(
            "Invalid or missing 'interval' data for PeriodicTask creation."
        )

    serializer = PeriodicTaskSerializer(data={**task_data, "interval": interval})
    if serializer.is_valid(raise_exception=True):
        periodic_task = serializer.save()
        return periodic_task
    else:
        return None


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

    def create(self, validated_data):
        periodic_task_data = validated_data.pop("periodic_task_data", None)
        notification_channels_data = validated_data.pop("notification_channel", [])
        interval_data = periodic_task_data.pop("interval", None)
        service = Service.objects.create(**validated_data)

        if notification_channels_data:
            service.notification_channel.set(notification_channels_data)

        if not periodic_task_data or not interval_data:
            raise ValueError(
                "Invalid or missing 'periodic_task_data' for Service creation."
            )
        # create interval schedule
        interval_serializer = IntervalScheduleSerializer(data=interval_data)
        if not interval_serializer.is_valid(raise_exception=True):
            raise ValueError("Invalid 'interval' data for PeriodicTask creation.")
        # overwrite periodic_task_data kwargs with service id
        periodic_task_data["kwargs"] = json.dumps({"service_id": service.id})
        # create periodic task
        periodic_task_data["interval"] = interval_data
        periodic_task_serializer = PeriodicTaskSerializer(data=periodic_task_data)
        if periodic_task_serializer.is_valid(raise_exception=True):
            periodic_task = periodic_task_serializer.save()
            service.periodic_task = (
                periodic_task  # Bind the PeriodicTask to the Service
            )
            service.save()

        return service

    def update(self, instance, validated_data):
        periodic_task_data = validated_data.pop("periodic_task_data", None)
        notification_channels_data = validated_data.pop("notification_channel", [])
        # Update other fields of Service
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if notification_channels_data:
            instance.notification_channel.set(notification_channels_data)

        if periodic_task_data:
            if hasattr(instance, "periodic_task") and instance.periodic_task:
                periodic_task = instance.periodic_task
            else:
                # Assuming you have a default creation mechanism or a similar function available
                periodic_task = create_periodic_task(instance, periodic_task_data)
                instance.periodic_task = periodic_task
                instance.save()

                # Now, update the periodic_task instance with new data
            PeriodicTaskSerializer().update(periodic_task, periodic_task_data)

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
