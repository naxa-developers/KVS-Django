# Generated by Django 2.0.5 on 2019-12-24 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20191223_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisabilityList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMemberCriteriaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_member_type', models.BooleanField(default=False)),
                ('member_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_member_criteria', to='core.FamilyMemberCriterialist')),
            ],
        ),
        migrations.CreateModel(
            name='GuideLineList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='HouseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('have_house', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Latrine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('have_latrine', models.BooleanField(default=False)),
                ('if_other_latrine', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PopulationChoiceData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_member_type', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RoadCapacityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('have_road', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WhoseOwnershipData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('have_ownership', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='household',
            name='house_type',
        ),
        migrations.RemoveField(
            model_name='household',
            name='if_other_toilet',
        ),
        migrations.RemoveField(
            model_name='household',
            name='occupation',
        ),
        migrations.RemoveField(
            model_name='household',
            name='road_capacity',
        ),
        migrations.RemoveField(
            model_name='household',
            name='toilet',
        ),
        migrations.RemoveField(
            model_name='household',
            name='whose_ownership',
        ),
        migrations.RemoveField(
            model_name='ownerfamily',
            name='family_member_criteria',
        ),
        migrations.RemoveField(
            model_name='ownerfamily',
            name='population_choices',
        ),
        migrations.AddField(
            model_name='facilities',
            name='have_facility',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fuel',
            name='have_fuel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='guideline',
            name='house_hold',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guideLine', to='core.HouseHold'),
        ),
        migrations.AddField(
            model_name='household',
            name='have_livestock',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='informationmedium',
            name='have_information',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='insurance',
            name='have_insurance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='occupation',
            name='house_hold',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='occupation', to='core.HouseHold'),
        ),
        migrations.AddField(
            model_name='occupation',
            name='if_occupation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='have_vehicle',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='warningmediumsuitablefordisaster',
            name='if_warning_medium',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='guideline',
            name='guideline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guideLine', to='core.GuideLineList'),
        ),
        migrations.AlterField(
            model_name='ownerfamily',
            name='age_group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='age_group', to='core.AgeGroupList'),
        ),
        migrations.AlterField(
            model_name='ownerfamily',
            name='education_level',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='family_education_level', to='core.EducationList'),
        ),
        migrations.AlterField(
            model_name='ownerfamily',
            name='gender',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='family_gender', to='core.GenderList'),
        ),
        migrations.AlterField(
            model_name='ownerfamily',
            name='involvement_in_occupation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='involvement', to='core.InvolvementList'),
        ),
        migrations.AlterField(
            model_name='ownerfamily',
            name='occupation_of_family',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='family_occupation', to='core.Occupation'),
        ),
        migrations.AlterField(
            model_name='technicalfield',
            name='gender',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='technical_gender', to='core.GenderList'),
        ),
        migrations.AddField(
            model_name='whoseownershipdata',
            name='house_hold',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='WhoseOwnershipData', to='core.HouseHold'),
        ),
        migrations.AddField(
            model_name='whoseownershipdata',
            name='ownership',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='WhoseOwnershipData', to='core.WhoseOwnershipList'),
        ),
        migrations.AddField(
            model_name='roadcapacitytype',
            name='house_hold',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='household_road', to='core.HouseHold'),
        ),
        migrations.AddField(
            model_name='roadcapacitytype',
            name='road',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='household_road', to='core.RoadCapacity'),
        ),
        migrations.AddField(
            model_name='populationchoicedata',
            name='owner_family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='population_choice', to='core.OwnerFamily'),
        ),
        migrations.AddField(
            model_name='populationchoicedata',
            name='population_choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='population_choice', to='core.PopulationChoicesList'),
        ),
        migrations.AddField(
            model_name='latrine',
            name='house_hold',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='latrine', to='core.HouseHold'),
        ),
        migrations.AddField(
            model_name='latrine',
            name='latrine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='latrine', to='core.LatrineList'),
        ),
        migrations.AddField(
            model_name='housetype',
            name='house_hold',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='house_type', to='core.HouseHold'),
        ),
        migrations.AddField(
            model_name='housetype',
            name='ownership',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.HouseTypeList'),
        ),
        migrations.AddField(
            model_name='familymembercriteriadata',
            name='owner_family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_member_criteria', to='core.OwnerFamily'),
        ),
    ]