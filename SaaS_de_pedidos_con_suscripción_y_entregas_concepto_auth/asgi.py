"""
ASGI config for SaaS_de_pedidos_con_suscripción_y_entregas_concepto_auth project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SaaS_de_pedidos_con_suscripción_y_entregas_concepto_auth.settings')

application = get_asgi_application()
