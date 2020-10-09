from django.db.models import CharField, BooleanField, EmailField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(self, login_email, name, is_organizer, is_staff, password=None):
        if not login_email:
            raise ValueError('Users must have an email address')

        user = self.model(
            login_email=self.normalize_email(login_email),
            name=name,
            is_organizer=is_organizer,
            is_staff=is_staff
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_email, name, password, is_staff=True, is_organizer=True):
        user = self.create_user(
            login_email,
            password=password,
            name=name,
            is_organizer=is_organizer,
            is_staff=is_staff
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    login_email = EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = CharField(max_length=30)
    is_organizer = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    city = CharField(max_length=30, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'login_email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
