# Generated by Django 4.1.1 on 2022-09-20 20:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_bid_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]