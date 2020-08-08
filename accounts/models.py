from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email,
        full_name, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email, password, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(
            email, password, **extra_fields)

    def get_id(self, id):
        user = self.model(id=id)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, default="Test")
    last_name = models.CharField(max_length=255, default="Test")
    image = models.FileField(null=True, blank=True, upload_to='upload/')
    birthday = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.full_name

    def get_image(self):
        return self.image

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})

    @property
    def full_name(self):
        return self.last_name + ' ' + self.first_name


class Post(models.Model):
    name = models.CharField(max_length=60)
    created_date = models.DateTimeField("Date created", auto_now=True,
                                        auto_now_add=False)
    author = models.ForeignKey(Profile, verbose_name="Автор поста",
                               related_name="author_post", default='',
                               on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, verbose_name="Получатель поста",
                                  null=True, blank=True,
                                  related_name="recipient_post",
                                  on_delete=models.CASCADE)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name