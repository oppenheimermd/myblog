# Generated by Django 4.0.3 on 2022-04-15 18:57

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_postimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_cover',
            field=models.ImageField(blank=True, upload_to=blog.models.rename_image),
        ),
        migrations.DeleteModel(
            name='PostImage',
        ),
    ]