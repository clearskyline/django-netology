# Generated by Django 4.1.3 on 2022-12-25 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField(default='')),
                ('status', models.TextField(choices=[('OPEN', 'Открыто'), ('CLOSED', 'Закрыто')], default='OPEN')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(blank=True, default=False, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdvFav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites_by_users', to='adv.advertisement')),
                ('users_favorites', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favourites_by_users', to=settings.AUTH_USER_MODEL, verbose_name='Users_added_to_favorites')),
            ],
        ),
        migrations.AddField(
            model_name='advertisement',
            name='favourites',
            field=models.ManyToManyField(related_name='fav_ads', through='adv.AdvFav', to=settings.AUTH_USER_MODEL),
        ),
    ]
