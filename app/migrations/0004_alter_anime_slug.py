# Generated by Django 5.1.1 on 2024-10-29 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_anime_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='Slug'),
        ),
    ]
