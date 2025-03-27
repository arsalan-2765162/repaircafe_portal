# Generated by Django 4.2.18 on 2025-03-22 19:34

import RepairCafe.models
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carbon_footprint_categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=123)),
                ('co2_emission_kg', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=128)),
                ('lastName', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(default='This is a Queue', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Repairer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='repairer_pictures/')),
            ],
        ),
        migrations.CreateModel(
            name='SharedPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(max_length=50, unique=True)),
                ('hashed_password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('roles', models.JSONField(default=list)),
                ('activerole', models.CharField(max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('isVolunteerCreated', models.BooleanField(default=False)),
                ('repairNumber', models.IntegerField(primary_key=True, serialize=False)),
                ('isCheckedOut', models.BooleanField(default=False)),
                ('itemName', models.CharField(max_length=128)),
                ('itemCategory', models.CharField(choices=[('ELECM', 'Electrical Mains'), ('ELEC', 'Electrical Low-Voltage/Battery'), ('TEXT', 'Clothing & Textiles'), ('CERA', 'Ceramics'), ('OTHER', 'Other')], max_length=128)),
                ('itemDescription', models.CharField(max_length=256)),
                ('repairStatus', models.CharField(choices=[('WAITING', 'Waiting'), ('WAITING_TO_JOIN', 'Waiting to Join Queue'), ('COMPLETED', 'Completed'), ('NEED_PAT', 'Needs PAT tested'), ('INCOMPLETE', 'Incomplete'), ('BEING_REPAIRED', 'Currently being Repaired')], default='WAITING_TO_JOIN', max_length=128)),
                ('incompleteReason', models.CharField(blank=True, choices=[('NOT_REP', 'Not repairable'), ('COM_BACK', 'Coming back next time'), ('TAKEN_HOME', 'Repairer has taken it home'), ('ADVICE_GIVEN', 'Advice given')], default=None, max_length=128, null=True)),
                ('position', models.IntegerField(blank=True, default=None, null=True)),
                ('time_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('checkinFormData', models.JSONField(blank=True, null=True)),
                ('checkoutFormData', models.JSONField(blank=True, null=True)),
                ('fault_cause', models.TextField(blank=True, null=True)),
                ('repair_solution', models.TextField(blank=True, null=True)),
                ('incomplete_cause', models.TextField(blank=True, null=True)),
                ('carbon_footprint_category', models.ForeignKey(default=RepairCafe.models.get_default_carbon_category, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='RepairCafe.carbon_footprint_categories')),
                ('customer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='RepairCafe.customer')),
                ('queue', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='RepairCafe.queue')),
                ('repairer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='RepairCafe.repairer')),
            ],
        ),
    ]
