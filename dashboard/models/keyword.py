from django.db import models

from dashboard.models.category import InfoObjectCategory


class Keyword(models.Model):
    word = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(InfoObjectCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.word
