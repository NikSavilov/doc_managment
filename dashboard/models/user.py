from django.contrib.auth.models import AbstractUser
from django.db import models

from dashboard.models.group import Group


class MyUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
