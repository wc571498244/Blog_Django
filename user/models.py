from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserProfile(AbstractUser):
    # icon = models.ImageField(upload_to='uploads/%Y/%d')
    yunIcon = models.CharField(max_length=300, default="")

    class Meta:
        db_table = 'UserProfile'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
