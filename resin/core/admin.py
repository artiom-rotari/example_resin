from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin

from .models import User, Group, BaseGroup


admin.site.unregister(BaseGroup)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass
