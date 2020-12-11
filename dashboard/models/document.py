from django.db import models

from dashboard.models.information_object import InformationObject


class Document(InformationObject):
    """ Любой файл, который может быть привязан к Информационному объекту """

    filename = models.CharField(max_length=256, null=True, blank=True)
    extension = models.CharField(max_length=10, null=True, blank=True)
    file = models.FileField()
    file_url = models.URLField(null=True, blank=True)  # Ссылка для документов хранящихся вне сервиса.
    size = models.IntegerField(null=True, blank=True)  # В байтах

    def __str__(self):
        return self.filename or self.file.name

    def get_mb_size(self):
        return round((self.size or 0) / 1024 / 1024, 1)
