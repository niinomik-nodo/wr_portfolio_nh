from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email!')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email,

        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
        

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255,unique=True)
    phone_number = models.IntegerField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/')

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'age']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
class UserActivateTokensManager(models.Manager):
    
    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now()

        ).first()
        user = user_activate_token.user
        user.is_active = True
        user.save()


class UserActivateTokens(models.Model):

    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )

    objects = UserActivateTokensManager()

    class Meta:
        db_table = 'user_activate_tokens'

@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs):
    print(str(uuid4))
    print(datetime.now() + timedelta(days=1))
    user_activate_token = UserActivateTokens.objects.create(
        user=instance, token=str(uuid4()),expired_at=datetime.now() + timedelta(days=1)

    )
    print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')




    