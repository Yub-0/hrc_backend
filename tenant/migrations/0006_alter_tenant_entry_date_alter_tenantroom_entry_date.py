# Generated by Django 4.1.5 on 2023-02-13 03:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0005_alter_tenant_entry_date_alter_tenantroom_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 13, 9, 38, 3, 132534)),
        ),
        migrations.AlterField(
            model_name='tenantroom',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 13, 9, 38, 3, 136531)),
        ),
    ]