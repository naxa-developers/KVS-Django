# Generated by Django 2.0.5 on 2019-12-23 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20191223_0919'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroupList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChronicIllnessList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMemberCriterialist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvolvementList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PopulationChoicesList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='household',
            name='building_completion_certificate',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='building_completion_certificate', to='core.PermitList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='education_level',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='education_level', to='core.EducationList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='ethnicity',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ethnicity', to='core.OwnershipList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='gender_of_house_owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gender', to='core.GenderList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='house_type',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='house_type', to='core.HouseTypeList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='mother_tongue',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mother_tongue', to='core.MotherTongueList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='received_building_permit',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_building_permit', to='core.PermitList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='religion',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='religion', to='core.ReligionList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='responder_gender',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responder_gender', to='core.GenderList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='road_capacity',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='road_type', to='core.RoadCapacity'),
        ),
        migrations.AlterField(
            model_name='household',
            name='road_type',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='road_type', to='core.RoadType'),
        ),
        migrations.AlterField(
            model_name='household',
            name='status_of_owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status', to='core.OwnershipList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='toilet',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toilet', to='core.LatrineList'),
        ),
        migrations.AlterField(
            model_name='household',
            name='whose_ownership',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='whose_ownership', to='core.WhoseOwnershipList'),
        ),
    ]