# Generated by Django 3.1.2 on 2020-12-28 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0026_auto_20201228_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userskills',
            name='expertise',
            field=models.CharField(choices=[('1', 'Novice'), ('11', 'Moderate'), ('111', 'Proficient'), ('1111', 'Expert')], default='1', max_length=4),
        ),
    ]
