from django.db import models

from dashboard.models.information_object import InformationObject


class Link(InformationObject):
    url = models.CharField(max_length=512)
    content = models.TextField(null=True, blank=True)
