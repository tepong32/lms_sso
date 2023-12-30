# Generated by Django 4.2.6 on 2023-12-08 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_leavecounter_additional_instances_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavecounter',
            name='total_approved_per_quarter',
            field=models.PositiveIntegerField(default=6, help_text="This count shows the default. Always check for 'additional_instances' for the actual computation of the max_allowed instances per_year and per_quarter.", verbose_name='Total Approved Per Quarter'),
        ),
        migrations.AlterField(
            model_name='leavecounter',
            name='total_instances_per_year',
            field=models.PositiveIntegerField(default=25, help_text="This count shows the default. Always check for 'additional_instances' for the actual computation of the max_allowed instances per_year and per_quarter.", verbose_name='Total Instances Per Year'),
        ),
    ]