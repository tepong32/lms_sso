# Generated by Django 4.2.6 on 2023-12-26 13:43

from django.db import migrations, models
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
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
                ('workgroup', models.CharField(choices=[('Secured Financial Support Team', 'SFST'), ('UnSecured Financial Support Team', 'UFST'), ('Australia Collections', 'AUH'), ('Australia', 'AU'), ('Philippines', 'PH'), ('Singapore', 'SG'), ('Marks & Spencer', 'MSS'), ('HSBC Repayment Services', 'HRS'), ('US', 'US'), ('CANADA', 'CANADA'), ('Outcome Testing Policy Adherence', 'OTPA')], default='Default', max_length=100, verbose_name='WorkGroup: ')),
                ('image', models.ImageField(blank=True, default='defaults/default_user_dp.png', upload_to=users.models.User.dp_directory_path, verbose_name='Photo')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
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
