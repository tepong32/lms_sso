# Generated by Django 4.2.6 on 2024-01-07 03:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WorkGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('---select one---', '---select one---'), ('Secured Financial Support Team', 'Secured Financial Support Team'), ('UnSecured Financial Support Team', 'UnSecured Financial Support Team'), ('Australia Collections', 'Australia Collections'), ('Australia', 'Australia'), ('Philippines', 'Philippines'), ('Singapore', 'Singapore'), ('Marks & Spencer', 'Marks & Spencer'), ('HSBC Repayment Services', 'HSBC Repayment Services'), ('US', 'United States'), ('CANADA', 'Canada'), ('Outcome Testing Policy Adherence', 'Outcome Testing Policy Adherence')], default='---select one---', max_length=80, verbose_name='Workgroup: ')),
                ('allowed_leaves_per_day', models.PositiveIntegerField(blank=True, default=20, help_text='\n            This will help with auto-approve leave requests.\n            Computation will be: allowed leaves - approved leaves for the day. If there are still available allowed_leaves_per_day instances, the leave requests will be auto-approved.\n            If there are none, the leave status will just be set to default: "Pending".\n        ', null=True)),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.manager')),
            ],
            options={
                'verbose_name_plural': 'Workgroups',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('staff_id', models.PositiveIntegerField(unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_advisor', models.BooleanField(default=True)),
                ('is_team_leader', models.BooleanField(default=False)),
                ('is_operations_manager', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('ext_name', models.CharField(blank=True, max_length=3, null=True, verbose_name='Extension')),
                ('image', models.ImageField(blank=True, default='defaults/default_user_dp.png', upload_to=users.models.User.dp_directory_path, verbose_name='Photo')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('workgroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.workgroup')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
    ]
