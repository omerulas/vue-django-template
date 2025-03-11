from django.db import models
from uuid import uuid1
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

# Create your models here.

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username, email: str, first_name:str, last_name:str, password:str, **kwargs):
        """
        Creates and saves a user with the given email and password
        if given is valid.
        * They are usually product user.
        """
        if not email: raise ValueError(_("A email must set for user.")) # User have to set an email.
        username = uuid1() # A unique username is automatically defines by the system avoid conflicts.
        email = self.normalize_email(email=email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, **kwargs)
        user.set_password(password) # Passwords must be hashed.
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password, **kwargs):
        """
        Creates and saves a super user working at the project with the given email and password
        if given is valid.
        * They are employee of project.
        """
        kwargs.setdefault('is_staff', True) # Super user have to gain is_staff=true.
        kwargs.setdefault('is_superuser', True) # Super user have to gain is_superuser=true.
        kwargs.setdefault('is_active', True) # Super user have to gain is_active=true.
        if kwargs.get('is_staff') is not True: raise ValueError(_('Super user must have is_staff=True'))
        if kwargs.get('is_superuser') is not True: raise ValueError(_('Super user must have is_superuser=True'))
        username = uuid1() # A unique username is automatically defines by the system avoid conflicts.
        return self.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"

    # Manual Assigment
    email = models.EmailField("E-posta", max_length=96, unique=True, blank=False, null=False, db_column="Eposta")
    first_name = models.CharField(verbose_name="Adı", max_length=36, blank=False, null=False, db_column="Adi")
    last_name = models.CharField(verbose_name="Soyadı", max_length=36, blank=False, null=False, db_column="Soyadi")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Auto Assigment
    joined = models.DateField("Katılım", auto_now_add=True, auto_now=False, blank=False, null=False)
    username = models.UUIDField(verbose_name="Kullanıcı Adı", default=uuid1, editable=False, unique=True, blank=True, null=True)    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_name_allias(self) -> str:
        return f"{self.first_name[0]}. {self.last_name}"
