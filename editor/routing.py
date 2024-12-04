# editor/routing.py
from django.urls import path
from .consumers import EditorConsumer

websocket_urlpatterns = [
    path('ws/editor/<str:doc_id>/', EditorConsumer.as_asgi()),
]
