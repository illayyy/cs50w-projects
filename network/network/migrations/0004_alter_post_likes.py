# Generated by Django 4.1.1 on 2022-11-11 10:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]