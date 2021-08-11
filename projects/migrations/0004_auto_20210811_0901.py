# Generated by Django 3.2.6 on 2021-08-11 09:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_auto_20210810_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='coworker',
        ),
        migrations.AddField(
            model_name='project',
            name='coworkers',
            field=models.ManyToManyField(blank=True, related_name='co_projects', to=settings.AUTH_USER_MODEL),
        ),
    ]