# Generated by Django 3.2.3 on 2021-06-20 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20210620_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polls',
            name='end_date',
            field=models.DateField(),
        ),
    ]
