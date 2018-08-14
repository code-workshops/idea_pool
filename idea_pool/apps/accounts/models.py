import uuid

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models


class User(AbstractUser):
    name = models.CharField(help_text='Name of user for non-traditional names.',
                            blank=True,
                            max_length=255)
    uid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('api:accounts-detail', kwargs={'pk': self.id})
