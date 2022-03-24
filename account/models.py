from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, nickname, password):
        user = self.model(
            username=username,
            nickname=nickname,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nickname, password):
        user = self.create_user(
            username=username,
            nickname=nickname,
            password=password,
        )
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=15, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.username
    # @property
    # def is_staff(self):
    #     return self.is_admin
