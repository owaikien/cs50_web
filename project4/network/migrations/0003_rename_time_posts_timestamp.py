# Generated by Django 4.2.1 on 2023-05-30 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_posts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='time',
            new_name='timestamp',
        ),
    ]
