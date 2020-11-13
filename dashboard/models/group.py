import uuid

from django.db import models

from doc_managment.settings import AUTH_USER_MODEL, MAIN_HOST, INVITE_LINK


class Group(models.Model):
    group_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    administrator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return "{name} ({adm})".format(name=self.name, adm=self.administrator.username)

    def get_invite(self):
        return INVITE_LINK.format(uuid=self.group_uuid)
