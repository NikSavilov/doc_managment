from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from dashboard.models.category import InfoObjectCategory
from dashboard.models.document import Document
from dashboard.models.group import Group
from dashboard.models.information_object import InformationObject
from dashboard.models.keyword import Keyword
from dashboard.models.link import Link
from dashboard.models.user import MyUser

admin.site.register(MyUser, UserAdmin)
admin.site.register(InfoObjectCategory)
admin.site.register(Document)
admin.site.register(Group)
admin.site.register(InformationObject)
admin.site.register(Keyword)
admin.site.register(Link)
