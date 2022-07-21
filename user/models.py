from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from rest_framework.permissions import
from oauth2_provider.models import Application


class MyUserManager(BaseUserManager):
    def create_user(self, name, contact_number, email, password=None):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            contact_number=contact_number,
            is_superuser=True)
        user.set_password(password)
        user.save(using=self._db)
        application = Application.objects.create(
            user=user,
            authorization_grant_type='password',
            client_type="public",
            name=user.name
        )
        return user

    def create_superuser(self, name, contact_number, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(name=name, contact_number=contact_number,
                                email=email, password=password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='email address', unique=True, )
    contact_number = models.BigIntegerField(default=None, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return False

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return False
