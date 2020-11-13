import randomcolor
from django.db import models
from django.utils.translation import gettext_lazy as _

from dashboard.models.category import InfoObjectCategory
from dashboard.models.group import Group


class InformationObject(models.Model):
    class Source(models.TextChoices):
        MA = 'MA', _("Manually added")
        VK = 'VK', 'Вконтакте'
        TG = 'TG', 'Telegram'
        MAIL = 'EM', _('E-mail')

    source = models.CharField(max_length=2, choices=Source.choices)
    connected_group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    source_id = models.CharField(max_length=256, null=True, blank=True)  # ID в источнике данных
    category = models.ForeignKey(InfoObjectCategory,  # Категории, привязанные к информационному объекту.
                                 null=True, blank=True,
                                 on_delete=models.CASCADE)

    def get_keywords(self, limit=3):
        keywords = list(self.category.keyword_set.all())
        if keywords.__len__() > limit:
            keywords = keywords[:limit]
        rand_color = randomcolor.RandomColor()
        k_dict = {key.word: {"color": rand_color.generate(luminosity='light')[0]} for key in keywords}
        return k_dict

    def __str__(self):
        return str(self.id)