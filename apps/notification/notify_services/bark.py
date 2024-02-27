import httpx
import pydantic


class Bark(pydantic.BaseModel):
    bark_endpoint: str = pydantic.Field(..., alias="bark-endpoint")

    # check if the bark endpoint is valid url
    @pydantic.field_validator("bark_endpoint", mode="before")
    def check_bark_endpoint(cls, v):
        if not v.startswith("http"):
            raise ValueError("Invalid bark endpoint")
        return v.rstrip("/") + "/"

    def send_notification(self, service, message):
        endpoint = self.bark_endpoint
        prepared_message = f"{service.name} - {message}"
        # Send the notification to the bark server
        # get the response and return it
        with httpx.Client(http2=True) as client:
            response = client.post(
                f"{endpoint}UptimeMonitor alert/{prepared_message}",
                headers={"Content-Type": "application/json"},
                json={"message": message},
            )
            if not response.is_success:
                raise ValueError(f"Failed to send notification: {response.text}")

            return True
