# Generated by Django 3.2.6 on 2021-08-11 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0004_auto_20210811_0901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('status', models.IntegerField(choices=[(1, 'todo'), (2, 'in progress'), (3, 'review'), (4, 'done')], null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_issues', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='projects.project')),
            ],
        ),
    ]