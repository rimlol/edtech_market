# Generated by Django 3.1.2 on 2020-11-07 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0014_auto_20201107_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='start_date',
            field=models.DateField(blank=True),
        ),
    ]
