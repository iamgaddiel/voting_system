# Generated by Django 3.2.4 on 2021-07-14 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judges', '0009_alter_judgespoll_voted_participant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judgeprofile',
            name='profile_picture',
            field=models.ImageField(default='profile.png', upload_to='judges_profile_picture.png'),
        ),
    ]
