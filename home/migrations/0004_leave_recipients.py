# Generated by Django 4.2.6 on 2023-11-15 05:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0003_alter_leavecounter_total_approved_per_quarter'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='recipients',
            field=models.ManyToManyField(related_name='leave_recipients', to=settings.AUTH_USER_MODEL),
        ),
    ]
