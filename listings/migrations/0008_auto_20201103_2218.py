# Generated by Django 3.1.2 on 2020-11-03 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0007_auto_20201102_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]