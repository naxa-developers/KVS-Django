# Generated by Django 2.0.5 on 2019-12-24 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20191224_0755'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChronicIllnessData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_chronic_illness', models.BooleanField(default=False)),
                ('if_other_chronic_illness', models.CharField(blank=True, max_length=200, null=True)),
                ('chronic_illness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chronic_illness', to='core.ChronicIllnessList')),
                ('owner_family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chronic_illness', to='core.OwnerFamily')),
            ],
        ),
        migrations.CreateModel(
            name='DisabilityData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_disability', models.BooleanField(default=False)),
                ('if_other_disability', models.CharField(blank=True, max_length=200, null=True)),
                ('owner_family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disability', to='core.OwnerFamily')),
                ('population_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disability', to='core.DisabilityList')),
            ],
        ),
    ]