# Generated by Django 3.1.2 on 2020-11-04 18:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0014_auto_20201031_2228'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Links',
            new_name='Link',
        ),
        migrations.RenameModel(
            old_name='Projects',
            new_name='Project',
        ),
    ]