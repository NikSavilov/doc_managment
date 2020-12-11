from django.contrib import admin

# Register your models here.

from dashboard.models.category import InfoObjectCategory, GroupInfoObjectCategory
from dashboard.models.document import Document
from dashboard.models.group import Group
from dashboard.models.information_object import InformationObject
from dashboard.models.keyword import Keyword
from dashboard.models.link import Link
from dashboard.models.profile import Profile

admin.site.register(InfoObjectCategory)
admin.site.register(GroupInfoObjectCategory)
admin.site.register(Document)
admin.site.register(Group)
admin.site.register(InformationObject)
admin.site.register(Keyword)
admin.site.register(Link)
admin.site.register(Profile)

