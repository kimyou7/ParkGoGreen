# Generated by Django 2.0.2 on 2018-05-16 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_auto_20180516_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='park',
            name='zip_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
