import httpx
import pydantic


class Bark(pydantic.BaseModel):
    bark_endpoint: str
    message: str

    def send_notification(self, service, message):
        endpoint = self.bark_endpoint
        prepared_message = f"{service.name} - {message}"
        # Send the notification to the bark server
        # get the response and return it
        with httpx.Client(http2=True) as client:
            response = client.post(
                f"{self.endpoint}/UptimeMonitor alert/{prepared_message}",
                headers=self._headers,
                json=message,
            )
            if not response.is_success:
                return False
            return True
