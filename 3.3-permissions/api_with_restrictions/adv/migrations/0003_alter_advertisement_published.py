# Generated by Django 4.1.3 on 2022-12-25 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adv', '0002_alter_advertisement_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='published',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
