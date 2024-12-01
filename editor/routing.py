from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/document/(?P<doc_id>\d+)/$', consumers.DocumentConsumer.as_asgi()),
]
