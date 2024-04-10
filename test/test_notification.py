import pytest
from rest_framework.exceptions import ValidationError
from apps.notification.serializers import NotificationChannelSerializer


@pytest.fixture
def valid_telegram_data():
    return {
        "name": "Test Channel",
        "details": {"token": "test_token", "chat_id": "test_chat_id"},
        "type": "telegram",
        "url": "http://example.com",
    }


@pytest.fixture
def valid_bark_data():
    return {
        "name": "Test Channel bark",
        "details": {
            "bark-endpoint": "http://example.com",
        },
        "type": "bark",
        "url": "http://example.com",
    }


@pytest.mark.django_db
def test_notification_channel_serializer_with_valid_data(
    valid_bark_data,
):
    serializer = NotificationChannelSerializer(data=valid_bark_data)
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_notification_channel_serializer_with_invalid_data(
    valid_bark_data,
):
    # Change the data to make it invalid
    valid_bark_data["type"] = "INVALID_TYPE"
    serializer = NotificationChannelSerializer(data=valid_bark_data)
    with pytest.raises(ValidationError):
        assert serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_notification_channel_serializer_with_invalid_detail():
    # Change the data to make it invalid
    valid_bark_data = {
        "name": "Test Channel bark",
        "details": {
            "NOT-REAL-bark-endpoint": "http://example.com",
        },
        "type": "bark",
        "url": "http://example.com",
    }
    serializer = NotificationChannelSerializer(data=valid_bark_data)
    with pytest.raises(ValidationError):
        assert serializer.is_valid(raise_exception=True)

    serializer = NotificationChannelSerializer(data=valid_bark_data)
    assert not serializer.is_valid()
    assert "(string='bark-endpoint'" in str(serializer.errors)
