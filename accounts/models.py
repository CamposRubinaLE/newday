# coding=utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from hashids import Hashids


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        user = self.model(email=email, is_active=True,
                          is_staff=is_staff, is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        if extra_fields.get('username'):
            extra_fields.pop('username')

        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    MALE = "m"
    FEMALE = "f"
    code = models.CharField(max_length=10, verbose_name="Código", null=True, blank=True)
    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=1, blank=True, choices=(
        (MALE, "male"), (FEMALE, "female")
    ))
    places = ArrayField(models.IntegerField(), blank=True, default=[])
    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def get_user_face(self):
        if self.social_auth.count() > 0:
            return True
        else:
            return False

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(User, self).save()
        if self.pk and not self.code:
            HASHIDS = Hashids(salt='User', min_length=10)
            self.code = HASHIDS.encode(self.pk)
            super(User, self).save(update_fields=['code'])
