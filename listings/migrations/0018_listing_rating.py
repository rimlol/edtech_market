# Generated by Django 3.1.2 on 2020-12-08 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.STAR_RATINGS_RATING_MODEL),
        ('listings', '0017_listing_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.STAR_RATINGS_RATING_MODEL),
        ),
    ]