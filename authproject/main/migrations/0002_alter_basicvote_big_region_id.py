# Generated by Django 5.0.4 on 2024-04-27 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicvote',
            name='big_region_id',
            field=models.IntegerField(),
        ),
    ]
