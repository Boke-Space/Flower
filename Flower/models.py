from django.db import models


# Create your models here.

class Recognition(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(max_length=0)
    img = models.CharField(max_length=100)
    result = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(max_length=0)
    temperature = models.CharField(max_length=20)
    humidty = models.CharField(max_length=20)
    gas = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)

class Card(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(max_length=0)
    uid = models.CharField(max_length=100)
    num = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)

