import httpx
import pydantic


class Telegram(pydantic.BaseModel):
    tg_token: str
    chat_id: str

    def send_notification(self, service, message):
        with httpx.Client(http2=True) as client:
            response = client.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={"chat_id": self.chat_id, "text": message},
            )
            if not response.is_success:
                return False
            return True
