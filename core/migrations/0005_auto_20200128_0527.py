# Generated by Django 2.0.5 on 2020-01-28 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_householddata_image_thumbnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='householddata',
            old_name='image_thumbnail',
            new_name='owned_land_image_thumbnail',
        ),
    ]