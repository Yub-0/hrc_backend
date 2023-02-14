# Generated by Django 4.1.5 on 2023-02-04 07:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 4, 13, 9, 15, 180084)),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='leave_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tenantroom',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 4, 13, 9, 15, 180084)),
        ),
    ]
