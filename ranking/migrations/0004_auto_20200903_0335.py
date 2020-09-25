# Generated by Django 3.0 on 2020-09-03 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0003_auto_20200902_0911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='household_field_mapping',
        ),
        migrations.AddField(
            model_name='question',
            name='map_to_field',
            field=models.CharField(default='a', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='map_to_model',
            field=models.CharField(default='a', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(max_length=200),
        ),
    ]
