# Generated by Django 2.2.6 on 2019-10-25 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('telephone_number', models.CharField(max_length=17)),
            ],
        ),
        migrations.CreateModel(
            name='HealthInsurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance_type', models.BooleanField()),
                ('insurance_number_type', models.CharField(max_length=20)),
                ('insurance_company_id', models.ForeignKey(on_delete=True, to='medaskApp.InsuranceCompany')),
            ],
            options={
                'unique_together': {('insurance_type', 'insurance_company_id')},
            },
        ),
    ]
