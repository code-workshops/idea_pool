from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models

from shortuuidfield import ShortUUIDField


class User(AbstractUser):
    name = models.CharField(help_text='Name of user for non-traditional names.',
                            blank=True,
                            max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=300, unique=True, null=True)
    uid = ShortUUIDField()
    avatar_url = models.URLField(default="default_avatar.jpg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('api:accounts-detail', kwargs={'pk': self.id})
