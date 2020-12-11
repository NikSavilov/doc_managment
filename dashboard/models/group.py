import uuid

from django.contrib.auth.models import User
from django.db import models

from doc_managment.settings import INVITE_LINK, INVITE_MESSAGE


class Group(models.Model):
    group_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128, blank=True)
    administrator = models.ForeignKey(User, on_delete=models.PROTECT)
    chat_id_vk = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{name} ({adm})".format(name=self.name, adm=self.administrator.username)

    def get_invite(self):
        return INVITE_LINK.format(uuid=self.group_uuid)

    def get_first_message(self):
        return INVITE_MESSAGE.format(uuid=str(self.group_uuid))
