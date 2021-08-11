# Generated by Django 3.2.6 on 2021-08-11 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_project_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.IntegerField(choices=[(1, 'todo'), (2, 'in progress'), (3, 'review'), (4, 'done')], default=1),
        ),
    ]
