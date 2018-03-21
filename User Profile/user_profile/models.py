from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class Customer(AbstractUser):

    email_confirmed = models.BooleanField(default=False)
    phone = PhoneNumberField(default=999999999, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)


    def __str__(self):
        return self.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Customer(user=instance)
        profile.save()
