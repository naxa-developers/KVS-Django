# Generated by Django 2.0.5 on 2019-12-23 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20191223_0610'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisasterList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]