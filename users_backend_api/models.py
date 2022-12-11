from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class MyUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using = self.db)

        return user

    def create_superuser(self, email, username, password=None, **kwargs):
        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            password = password,
            **kwargs
        )
        user.user_category = 'Mod'
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self.db)
        return user


class MyUser(AbstractBaseUser):
    USER_CATEGORY = (
        ('User', 'User'),
        ('Mod', 'Moderator'),
    )

    username = models.CharField(verbose_name="Username", max_length=25, primary_key=True)
    email = models.EmailField(verbose_name="Email Address", max_length=200, null=False, unique=True)
    first_name = models.CharField(verbose_name="First Name", max_length=200, blank=True)
    middle_name = models.CharField(verbose_name="Middle Name", max_length=200, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=200, blank=True)
    phone = models.BigIntegerField(verbose_name="Contact Number", null=True, blank=True)
    age = models.IntegerField(verbose_name="Age", null=True, blank=True)
    gender = models.CharField(verbose_name="Gender", max_length=200, null=True, blank=True)
    user_category = models.CharField(verbose_name="User Category", choices=USER_CATEGORY, default='User', max_length=200)
    profile_pic = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/')

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'password']

    objects = MyUserManager()

    def __str__(self):
        return self.username
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True


class OTPModel(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, verbose_name="Verification Code")
    creation_date_time = models.DateTimeField(
        auto_now_add=True,
        help_text="The timestamp of creation of otp."
    )
