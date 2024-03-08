from django_celery_beat.models import PeriodicTask
from rest_framework import serializers

from .models import Service
from ..monitoring.serializers import PeriodicTaskSerializer
from ..notification.models import NotificationChannel


def get_periodic_task_choices():
    # Assuming you have a model `PeriodicTask` from which to fetch the IDs
    return [(task.id, task.name) for task in PeriodicTask.objects.all()]


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    periodic_task_id = serializers.ChoiceField(
        choices=get_periodic_task_choices(),
        write_only=True,
        allow_null=True,
        required=False,
    )
    periodic_task = serializers.JSONField(
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
            "periodic_task_id",
            "periodic_task",
            "updated_at",
        )

        extra_kwargs = {
            "periodic_task": {"required": False},
            "updated_at": {"read_only": True},
            "notification_channel": {"required": False, "allow_null": True},
        }

    def validate(self, data):
        """
        Check that either periodic_task_id or periodic_task is provided, not both.
        """
        periodic_task_id = data.get("periodic_task_id")
        periodic_task_data = data.get("periodic_task")

        if periodic_task_id and periodic_task_data:
            raise serializers.ValidationError(
                "Please provide either a periodic_task_id or periodic_task data, not both."
            )
        if not periodic_task_id and not periodic_task_data:
            raise serializers.ValidationError(
                "You must provide either a periodic_task_id or periodic_task data."
            )

        return data

    def create(self, validated_data):
        periodic_task_id = validated_data.pop("periodic_task_id", None)
        periodic_task_data = validated_data.pop("periodic_task", None)
        periodic_task = None
        notification_channels_data = validated_data.pop("notification_channel", [])

        if periodic_task_id:
            periodic_task = PeriodicTask.objects.get(id=periodic_task_id)
        elif periodic_task_data:
            periodic_task_serializer = PeriodicTaskSerializer(data=periodic_task_data)
            if periodic_task_serializer.is_valid(raise_exception=True):
                periodic_task = periodic_task_serializer.save()

        service = Service.objects.create(**validated_data, periodic_task=periodic_task)
        if notification_channels_data:
            # Assuming notification_channels_data is a list of PKs
            # e.g. [1,3]
            notification_channels = NotificationChannel.objects.filter(
                id__in=notification_channels_data
            )
            service.notification_channel.set(notification_channels)

        return service

    def update(self, instance, validated_data):
        periodic_task_id = validated_data.pop("periodic_task_id", None)
        periodic_task_data = validated_data.pop("periodic_task", None)
        notification_channels_data = validated_data.pop("notification_channel", [])

        if periodic_task_id:
            instance.periodic_task = PeriodicTask.objects.get(id=periodic_task_id)
        elif periodic_task_data:
            if instance.periodic_task:
                periodic_task_serializer = PeriodicTaskSerializer(
                    instance.periodic_task, data=periodic_task_data
                )
            else:
                periodic_task_serializer = PeriodicTaskSerializer(
                    data=periodic_task_data
                )
            if periodic_task_serializer.is_valid(raise_exception=True):
                instance.periodic_task = periodic_task_serializer.save()
        elif not periodic_task_id and instance.periodic_task:
            pass

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Update notification channels
        if notification_channels_data:
            instance.notification_channel.set(notification_channels_data)

        return instance
