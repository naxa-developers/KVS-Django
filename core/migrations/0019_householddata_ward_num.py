# Generated by Django 2.0.5 on 2020-01-01 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20200101_0507'),
    ]

    operations = [
        migrations.AddField(
            model_name='householddata',
            name='ward_num',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]