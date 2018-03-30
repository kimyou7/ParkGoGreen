# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Park(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class Status(models.Model):
    current_status = models.CharField(max_length=200)

    def __str__(self):
        return self.current_status
