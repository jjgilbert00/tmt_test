from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractUser):
    username = models.CharField(
        _("username"), 
        max_length=150, 
        help_text=_(
            "150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        unique=False, 
        blank=True,
        validators=[AbstractUser.username_validator],
    )
    email = models.EmailField(_("email address"), unique=True, blank=False)

    is_admin = models.BooleanField(default=False)
    avatar = models.ImageField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self) -> str:
        return super().get_full_name()
    
    def get_username(self) -> str:
        return super().get_username()
    
    @property
    def is_authenticated(self) -> bool:
        return super().is_authenticated

