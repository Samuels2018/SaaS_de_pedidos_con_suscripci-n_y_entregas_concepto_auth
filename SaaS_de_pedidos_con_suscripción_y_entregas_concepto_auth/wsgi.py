"""
WSGI config for SaaS_de_pedidos_con_suscripción_y_entregas_concepto_auth project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SaaS_de_pedidos_con_suscripción_y_entregas_concepto_auth.settings')

application = get_wsgi_application()
