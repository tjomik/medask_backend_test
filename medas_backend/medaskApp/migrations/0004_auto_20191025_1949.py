# Generated by Django 2.2.6 on 2019-10-25 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medaskApp', '0003_auto_20191025_1947'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='healthinsurance',
            unique_together={('insurance_type', 'company_name')},
        ),
    ]
