from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import pytz
class CustomUser(AbstractUser):
    is_mail_verified = models.BooleanField(default=False)
    is_account_active= models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=datetime.now(pytz.timezone('Europe/Madrid')))
    date_last_ban = models.DateTimeField(default=datetime.now(pytz.timezone('Europe/Madrid')))
    number_of_bans = models.IntegerField(default=0)
    is_ban_right_now = models.BooleanField(default=False)
    def __str__(self):
        return self.email
