from django.db import models


class InfoObjectCategory(models.Model):
    """ Категория для информационных объектов """
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title
