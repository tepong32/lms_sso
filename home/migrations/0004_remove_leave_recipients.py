# Generated by Django 4.2.6 on 2023-11-22 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_leave_recipients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='recipients',
        ),
    ]
