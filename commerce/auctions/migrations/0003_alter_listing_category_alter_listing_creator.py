# Generated by Django 4.1.1 on 2022-09-19 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='category_listings', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
