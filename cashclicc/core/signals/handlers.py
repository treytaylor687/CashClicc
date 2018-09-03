# grap_main/signals/handlers.py

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.contrib.auth.models import User
from django.dispatch import receiver


def payment_complete(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != "info@cashclicc.com":
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received etc. are all what you expect.

        # Undertake some action depending upon `ipn_obj`.
        User.objects.filter(username=ipn_obj.custom)[0].profile.add_tokens(int(ipn_obj.item_name.partition(" ")[0]))

valid_ipn_received.connect(payment_complete)