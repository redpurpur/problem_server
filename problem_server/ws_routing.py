from main.ws_consumer import SubmissionStatusConsumer
from django.urls import path


websocket_urlpatterns = [
    path(r'check_submission_status/<int:submission_id>/',
         SubmissionStatusConsumer.as_asgi(), name='submission_status'),
]
