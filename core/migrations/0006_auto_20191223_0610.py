# Generated by Django 2.0.5 on 2019-12-23 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20191223_0546'),
    ]

    operations = [
        migrations.CreateModel(
            name='HouseDamageList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='damagetype',
            name='damage_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='damage_type', to='core.DamageList'),
        ),
        migrations.AlterField(
            model_name='damagetype',
            name='damages',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='damagetype',
            name='if_house_damage_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='damage_type', to='core.HouseDamageList'),
        ),
    ]
