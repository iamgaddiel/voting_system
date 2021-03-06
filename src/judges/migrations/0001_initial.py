# Generated by Django 3.2.3 on 2021-06-01 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('polls', '0004_rename_link_polls_address'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JudgeProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('profile_picture', models.ImageField(default='profile.png', upload_to='judges_profile_picture')),
                ('educational_qualification', models.CharField(choices=[('ND', 'ND'), ('HND', 'HND'), ('BSC', 'BSC'), ('MSc', 'MSc'), ('Phd', 'Phd')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JudgesPolls',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('project_link', models.CharField(blank=True, default='', max_length=100)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('judge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judges.judgeprofile')),
                ('polls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.polls')),
            ],
        ),
    ]
