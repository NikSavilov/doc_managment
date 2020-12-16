import randomcolor
from django.db import models
from model_utils.managers import InheritanceManager


class InfoObjectCategory(models.Model):
    """ Категория для информационных объектов """
    objects = InheritanceManager()
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title

    def get_keywords(self, limit=3):
        from dashboard.models import Keyword
        keywords = Keyword.objects.filter(category=self)
        if keywords.__len__() > limit:
            keywords = keywords[:limit]
        rand_color = randomcolor.RandomColor()

        k_dict = {key.word: {"color": rand_color.generate(luminosity='light')[0]} for key in keywords}

        return k_dict


class GroupInfoObjectCategory(InfoObjectCategory):
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
