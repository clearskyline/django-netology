# Generated by Django 4.1.3 on 2022-12-12 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0003_rename_sensor_measurement_sensor_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurement',
            old_name='sensor_id',
            new_name='sensor',
        ),
    ]
