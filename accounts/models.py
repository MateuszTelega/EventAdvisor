from django.db import models
from django.db.models import CharField, IntegerField, EmailField, CASCADE
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager


class User(AbstractBaseUser):
    REQUIRED_FIELDS = ('name',)
    # user = models.OneToOneField(User, default=None, null=True, on_delete=CASCADE)
    login_email = EmailField(null=False, unique=True)
    name = CharField(max_length=30, null=False)
    is_organizer = IntegerField(default=0)
    city = CharField(max_length=30, null=True)

    USERNAME_FIELD = 'login_email'

    objects = UserManager()

    def __str__(self):
        return f"{self.name}"
