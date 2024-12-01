"""
ASGI config for DPCS_collab_text_editor project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from editor import consumers  


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DPCS_collab_text_editor.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Add WebSocket URL routing here
            path('ws/editor/<int:doc_id>/', consumers.EditorConsumer.as_asgi()),
        ])
    ),
})
