# Generated by Django 4.2.6 on 2023-12-05 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_first_name_alter_profile_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='operations_manager',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='team_leader',
        ),
    ]