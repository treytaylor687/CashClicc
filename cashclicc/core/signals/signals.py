# grap_main/signals/handlers.py

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.contrib.auth.models import User
from django.dispatch import receiver
