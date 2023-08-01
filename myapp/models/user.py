from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from myapp.models.abstracts.base import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        first_name = extra_fields.get("first_name", None)
        last_name = extra_fields.get("last_name", None)

        if not email:
            raise ValueError("Email is required.")
        if not first_name:
            raise ValueError("First name is required.")
        if not last_name:
            raise ValueError("Last name is required.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        first_name = extra_fields.get("first_name", None)
        last_name = extra_fields.get("last_name", None)

        if not email:
            raise ValueError("Email is required.")
        if not first_name:
            raise ValueError("First name is required.")
        if not last_name:
            raise ValueError("Last name is required.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be staff.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be superuser")

        return self.create_user(email, password, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """Models a single application user."""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=35, blank=False, null=False, db_index=True)
    last_name = models.CharField(max_length=35, blank=False, null=False, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_active = models.DateTimeField(auto_now=True, null=True)
    last_login = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self) -> str:
        return str(self.email)

    def to_dict(self, exclude=None, include=None):
        default_exclude = ["password", "is_staff", "is_superuser"]
        if exclude:
            exclude.extend(default_exclude)
        if not exclude:
            exclude = default_exclude
        return super().to_dict(exclude, include)
