# Generated by Django 3.2.3 on 2021-05-31 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0006_auto_20210531_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantpolls',
            name='project_link',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
