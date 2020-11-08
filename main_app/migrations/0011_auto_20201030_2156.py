# Generated by Django 3.1.2 on 2020-10-30 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20201019_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='education',
            old_name='student',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='projects',
            old_name='owner',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='education',
            name='id',
        ),
        migrations.AddField(
            model_name='education',
            name='edu_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
