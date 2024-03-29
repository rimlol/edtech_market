# Generated by Django 3.1.2 on 2020-11-08 10:31

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('listings', '0016_auto_20201107_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
