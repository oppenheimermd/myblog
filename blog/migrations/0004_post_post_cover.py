# Generated by Django 4.0.3 on 2022-04-19 16:45

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_cover',
            field=models.ImageField(blank=True, upload_to=blog.models.rename_image),
        ),
    ]
