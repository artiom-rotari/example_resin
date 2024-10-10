from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager, Group as BaseGroup
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        return super().create_superuser(username=email, email=email, password=password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    email = models.EmailField(_("email address"), unique=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class Group(BaseGroup):
    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        proxy = True
