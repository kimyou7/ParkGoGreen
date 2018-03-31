# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class Park(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    maps_string = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.maps_string:
            self.maps_string = "https://www.google.com/maps/embed/v1/place?key=AIzaSyBMDvz4zozQwoRPNcXrFX8OCGDp6c1FL7E&q=" + self.name.replace(" ", "+")
        super(Park, self).save(*args, **kwargs)


class Category(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class Status(models.Model):
    current_status = models.CharField(max_length=200)

    def __str__(self):
        return self.current_status


class Report(models.Model):
    sub_date = models.DateTimeField('date submitted')
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='issues')
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    park = models.ForeignKey(Park, on_delete=models.CASCADE)

    def __str__(self):
        return self.park.name + " " + self.sub_date
