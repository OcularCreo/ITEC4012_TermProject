# Generated by Django 4.2.6 on 2023-10-31 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discoverapp', '0003_alter_recipe_ingreds_alter_recipe_nutrition_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='testTable2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
        ),
    ]
