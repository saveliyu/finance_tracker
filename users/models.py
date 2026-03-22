from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from family.models import FamilyMember
from django.core.exceptions import ObjectDoesNotExist


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, name=None, color=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(name=name, username=username, color=color, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, name=None, color=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, name, color, **extra_fields)


class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)

    objects = CustomUserManager()

    @property
    def get_family_object(self):
        member = self.get_family_member
        return member.family if member else None

    @property
    def get_family_member(self):
        try:
            return self.family_member
        except ObjectDoesNotExist:
            return None

    @property
    def get_family_members(self):
        family = self.get_family_object
        return family.members.all() if family else FamilyMember.objects.none()

    def __str__(self):
        return self.username
