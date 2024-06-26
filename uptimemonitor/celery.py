import os

from celery import Celery
from dotenv import load_dotenv
from pathlib import Path

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uptimemonitor.settings")
dotenv_path = Path(".env.dev")

print("could not load .env.dev file for CELERY!") if not load_dotenv(
    dotenv_path=dotenv_path
) else print("found .env.dev file for CELERY!")
app = Celery(
    "uptimemonitor",
    broker=f"amqp://{os.getenv("RABBITMQ_DEFAULT_USER", "myrabbituser")}:"
    f"{os.getenv("RABBITMQ_DEFAULT_PASS", "myrabbitpassword")}@{os.getenv("RABBITMQ_URL", "rabbitmq:5672")}//",
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
