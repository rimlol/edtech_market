# Generated by Django 3.1.2 on 2020-10-30 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_category_russian_alias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='slug',
            field=models.SlugField(blank=True, max_length=70),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='slug',
            field=models.SlugField(blank=True, max_length=70),
        ),
    ]
