# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# Each model should have a __str__ method that returns a string when an instance of the model is referenced.

import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User


# Model of the park, creates Google Maps url when save() is called
class Park(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    maps_string = models.CharField(max_length=1000, null=True, blank=True)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    # Override save function to create and store the Google Maps string from the provided park name.
    def save(self, *args, **kwargs):
        if not self.maps_string:
            self.maps_string = "https://www.google.com/maps/embed/v1/place?key=AIzaSyBMDvz4zozQwoRPNcXrFX8OCGDp6c1FL7E&q=" + self.name.replace(" ", "+")
        super(Park, self).save(*args, **kwargs)


# Category of the report
class Category(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


# Status of the report
class Status(models.Model):
    current_status = models.CharField(max_length=200)

    def __str__(self):
        return self.current_status


# Report model. Automatically takes the current time from the set Timezone. Description and image must be included
# by whoever creates it. Type, status, and the park are chosen from drop down menus. The user should be set by grabbing
# whoever is logged in. The image will be saved to the csc648-team13/media/photos folder. When the report is saved,
# a thumbnail is created, saved to the csc648-team13/media/thumbs folder, and the url is added to the thumbnail field.
class Report(models.Model):
    sub_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='photos', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbs', editable=False, null=True)
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    park = models.ForeignKey(Park, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.park.name + " " + str(self.sub_date)

    # Override save function to create thumbnail.
    def save(self, *args, **kwargs):
        if not self.image.closed:
            if not self.make_thumbnail():
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(Report, self).save(*args, **kwargs)

    # make_thumbnail and save functions created by users xjtian and ziiirp on stackoverflow
    # https://stackoverflow.com/questions/23922289/django-pil-save-thumbnail-version-right-when-image-is-uploaded
    def make_thumbnail(self):
        photo = Image.open(self.image)
        photo.thumbnail((250, 250), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False

        temp_thumb = BytesIO()
        photo.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True
