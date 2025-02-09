# myapp/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/appointments/(?P<appointment_id>\w+)/$', consumers.AppointmentConsumer.as_asgi()),
]