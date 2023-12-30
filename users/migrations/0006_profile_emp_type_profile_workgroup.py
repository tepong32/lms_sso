 Generated by Django 4.2.6 on 2023-12-05 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_emp_type_remove_profile_workgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='emp_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.employeetype'),
        ),
        migrations.AddField(
            model_name='profile',
            name='workgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.workgroup'),
        ),
    ]
