# Generated by Django 3.1.2 on 2020-12-10 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0024_userskills_expertise'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userskills',
            name='id',
        ),
        migrations.AddField(
            model_name='userskills',
            name='skill_user_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userskills',
            name='expertise',
            field=models.IntegerField(choices=[(0, 'Low'), (1, 'Normal'), (2, 'High')], default=0),
        ),
    ]
