# Generated by Django 2.0.5 on 2019-12-24 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20191224_1020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='household',
            old_name='indx',
            new_name='index',
        ),
    ]
