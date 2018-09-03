from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client
from random import randint
from django.core.exceptions import MiddlewareNotUsed
import logging
import json
from ..settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER


class Donation(models.Model):
    current_donations = models.PositiveIntegerField(default=0)

    def increase_donations(self):
        self.current_donations += 1
        self.save()

    def get_total_donation(self):
        dollars = self.current_donations // 100
        cents = (self.current_donations % 100)
        if cents < 10:
            cents = "0" + str(self.current_donations % 100)
        return str(dollars) + "." + str(cents)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = models.PositiveIntegerField(default=10)
    balance = models.PositiveIntegerField(default=0)
    validation_token = models.PositiveIntegerField(null=True)
    phone_number = models.CharField(null=True, max_length=10)

    def __str__(self):
        return str(self.user)

    def get_tokens(self):
        return self.tokens

    def set_validation_token(self, token):
        self.validation_token = token

    def get_validation_token(self):
        return self.validation_token

    def add_tokens(self, tokens_to_add):
        self.tokens = self.tokens + tokens_to_add
        self.save()

    def use_token(self):
        self.tokens -= 1
        self.save()

    def edit_balance(self, change):
        self.balance += change
        self.save()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Game(models.Model):
    amount = models.IntegerField(blank=False)
    current_time = models.DateTimeField(blank=False, auto_now=True)
    end_time = models.DateTimeField(blank=False)
    current_top_user = models.CharField(max_length=50, default="NO TOP USER!")
    status = models.PositiveIntegerField(blank=False, default=1)

    #def update_game(self, name):
        #username = str(User.objects.filter(username=name.user)[0])
        #self.current_top_user = username
        #time_d = self.end_time - self.current_time
        #if time_d.seconds < 10:
        #    self.end_time += timedelta(seconds=(10 - time_d.seconds))
        #self.save()
        #if self.current_top_user == username:
        #    name.use_token()


    def get_top_user(self):
        return self.current_top_user

    def update_current_time(self):
        self.save()

    def update_status(self):
        if self.status == 1:
            self.status = 0
        else:
            self.status = 1

    def time_remaining(self):
        if self.current_time > self.end_time and self.status == 1:
            self.update_status()
            if self.current_top_user == "NO TOP USER!":
                self.save()
                return "quit"
            User.objects.filter(username=self.current_top_user)[0].profile.edit_balance(self.amount)
            self.save()
            return "quit"

        else:
            time_delta = self.end_time - self.current_time
            seconds = time_delta.total_seconds()
            #hours = "0" + str(time_delta.seconds // 3600) if (time_delta.seconds // 3600) < 10 else (time_delta.seconds // 3600)
            #minutes = "0" + str((time_delta.seconds % 3600) // 60) if ((time_delta.seconds % 3600) // 60) < 10 else ((time_delta.seconds % 3600) // 60)
            #seconds = "0" + str((time_delta.seconds % 3600) % 60) if ((time_delta.seconds % 3600) % 60) < 10 else ((time_delta.seconds % 3600) % 60)
            #return str(hours) + ":" + str(minutes) + ":" + str(seconds)
            return '%02d:%02d:%02d' % (seconds / 3600, seconds / 60 % 60, seconds % 60)


logger = logging.getLogger(__name__)

MESSAGE = """[This is a test] ALERT! It appears the server is having issues.
Exception: %s. Go to: http://newrelic.com for more details."""

NOT_CONFIGURED_MESSAGE = """Cannot initialize Twilio notification
middleware. Required enviroment variables TWILIO_ACCOUNT_SID, or
TWILIO_AUTH_TOKEN or TWILIO_NUMBER missing"""


def load_admins_file():
    with open('config/administrators.json') as adminsFile:
        admins = json.load(adminsFile)
        return admins


def load_twilio_config():
    twilio_account_sid = TWILIO_ACCOUNT_SID
    twilio_auth_token = TWILIO_AUTH_TOKEN
    twilio_number = TWILIO_NUMBER

    if not all([twilio_account_sid, twilio_auth_token, twilio_number]):
        logger.error(NOT_CONFIGURED_MESSAGE)
        raise MiddlewareNotUsed

    return (twilio_number, twilio_account_sid, twilio_auth_token)


class MessageClient(object):
    def __init__(self):
        (twilio_number, twilio_account_sid,
         twilio_auth_token) = load_twilio_config()

        self.twilio_number = twilio_number
        self.twilio_client = Client(twilio_account_sid,
                                              twilio_auth_token)

    def generate_token(self):
        return randint(111111, 999999)

    def send_message(self, body, to):
        self.twilio_client.messages.create(body=body, to=to,
                                           from_=self.twilio_number,
                                           )


class TwilioNotificationsMiddleware(object):
    def __init__(self):
        self.administrators = load_admins_file()
        self.client = MessageClient()

    def process_exception(self, request, exception):
        exception_message = str(exception)
        message_to_send = MESSAGE % exception_message

        for admin in self.administrators:
            self.client.send_message(message_to_send, admin['phone_number'])