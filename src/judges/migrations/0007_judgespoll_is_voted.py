# Generated by Django 3.2.3 on 2021-06-13 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judges', '0006_alter_judgespoll_voted_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='judgespoll',
            name='is_voted',
            field=models.BooleanField(default=False),
        ),
    ]