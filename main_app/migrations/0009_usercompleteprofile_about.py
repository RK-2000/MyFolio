# Generated by Django 3.1.2 on 2020-10-19 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_education_links_projects_usercompleteprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercompleteprofile',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
