# Generated by Django 3.1.2 on 2020-10-31 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]
