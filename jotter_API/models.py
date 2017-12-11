# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):

    class Meta:
        app_label='jotter_API'
    def __str__(self):
        return self.username


class Note(models.Model):

    owner = models.ForeignKey(User, null=True)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text
        # a more apt way of representing this


class Image(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, to_field='id')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image.name