# Generated by Django 4.2.6 on 2023-12-05 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discoverapp', '0015_userrecipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecipe',
            name='playlist_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
