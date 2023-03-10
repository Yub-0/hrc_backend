# Generated by Django 4.1.5 on 2023-02-01 06:59

import datetime
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('house', '0004_house_floors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('permanent_address', models.CharField(max_length=25, null=True)),
                ('age', models.IntegerField(null=True)),
                ('contact_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Left', 'Left'), ('Hold', 'Hold')], default='Active', max_length=25)),
                ('entry_date', models.DateTimeField(default=datetime.datetime(2023, 2, 1, 12, 44, 45, 745229))),
                ('leave_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TenantRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Left', 'Left'), ('Hold', 'Hold'), ('Changed', 'Changed')], default='Active', max_length=25)),
                ('entry_date', models.DateTimeField(default=datetime.datetime(2023, 2, 1, 12, 44, 45, 745229))),
                ('leave_date', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.room')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='RoomChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(null=True)),
                ('from_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_room', to='house.room')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant')),
                ('to_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_name', to='house.room')),
            ],
        ),
    ]
