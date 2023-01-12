# Generated by Django 4.1.3 on 2022-12-03 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_tag_alter_article_options_scope'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(related_name='articles', through='articles.Scope', to='articles.tag'),
        ),
        migrations.AlterField(
            model_name='scope',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scopes', to='articles.article'),
        ),
        migrations.AlterField(
            model_name='scope',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scopes', to='articles.tag'),
        ),
    ]
