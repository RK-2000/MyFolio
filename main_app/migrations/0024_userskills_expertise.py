# Generated by Django 3.1.2 on 2020-12-09 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_userskills'),
    ]

    operations = [
        migrations.AddField(
            model_name='userskills',
            name='expertise',
            field=models.CharField(default=0, max_length=1),
            preserve_default=False,
        ),
    ]
