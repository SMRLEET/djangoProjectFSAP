import os
from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models



# Create your models here.
from djangoProjectFSAP import settings



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_moder = models.BooleanField(default=False)
    registrationDate = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']



class CustomAccountUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        user = self.model(email=email, username=username, password=password)
        user.set_password(password)
        user.is_moder = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.model(email=email, username=username, password=password)
        user.set_password(password)
        user.is_moder = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username_):
        print(username)
        return self.get(username=username_)


def wrapper(instance, filename):
    ext = filename.split('.')[-1]
    author = "pid_%s" % (instance.author.id,)
    if instance.pk:
        complaint_id = "cid_%s" % (instance.pk,)
        filename = '{}{}.{}'.format(author, complaint_id, ext)
    else:
        random_id = "rid_%s" % (uuid4().hex,)
        filename = '{}{}.{}'.format(author, random_id, ext)
    return os.path.join(settings.FILE_ROOT, filename)

class Genere(models.Model):
    genere_id = models.AutoField(primary_key=True)
    genere_name = models.CharField(max_length=500, unique=True)


class Instrument(models.Model):
    instrument_id = models.AutoField(primary_key=True)
    instrument_name = models.CharField(max_length=60, unique=True)


class Sytheseizer(models.Model):
    sytheseizer_id = models.AutoField(primary_key=True)
    sytheseizer_name = models.CharField(max_length=60, unique=True)


class SamplePack(models.Model):
    class Meta:
        unique_together = (('name', 'author'))
    sp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    genere_id = models.ForeignKey(Genere, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    path = models.FileField(upload_to=wrapper, max_length=100, blank=True)


class Sample(models.Model):
    class Meta:
        unique_together = (('sample_id', 'sp_id'))
    sample_id = models.AutoField(primary_key=True)
    sp_id = models.ForeignKey(SamplePack, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    instrument_id = models.ForeignKey(Instrument, on_delete=models.CASCADE)


class PresetPack(models.Model):
    class Meta:
        unique_together = (('name', 'sytheseizer_id', 'author'))

    pp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    genere_id = models.ForeignKey(Genere, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sytheseizer_id = models.ForeignKey(Sytheseizer, on_delete=models.CASCADE)
    dateAdded = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    path = models.FileField(upload_to=wrapper, max_length=100,blank=True)


class Preset(models.Model):
    class Meta:
        unique_together = (('name', 'pp_id'))

    preset_id = models.AutoField(primary_key=True)
    pp_id = models.ForeignKey(PresetPack, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    instrument_id = models.ForeignKey(Instrument, on_delete=models.CASCADE)


class FavoriteSamplePacks(models.Model):
    class Meta:
        unique_together = ('user', 'sp_id')

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sp_id = models.ForeignKey(SamplePack, on_delete=models.CASCADE)


class FavoritePresetPacks(models.Model):
    class Meta:
        unique_together = ('user', 'pp_id')
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pp_id = models.ForeignKey(PresetPack, on_delete=models.CASCADE)

