# Generated by Django 2.0.5 on 2020-01-28 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_aboutproject_image_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='overallsystemfeatures',
            name='image_thumbnail',
            field=models.ImageField(blank=True, editable=False, null=True, upload_to='thumbs'),
        ),
        migrations.AlterField(
            model_name='overallsystemfeatures',
            name='feature1',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='overallsystemfeatures',
            name='feature2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='overallsystemfeatures',
            name='feature3',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='overallsystemfeatures',
            name='feature4',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='overallsystemfeatures',
            name='feature5',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='overallsystemfeatures',
            name='feature6',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='overallsystemfeatures',
            name='feature7',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='overallsystemfeatures',
            name='feature8',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
