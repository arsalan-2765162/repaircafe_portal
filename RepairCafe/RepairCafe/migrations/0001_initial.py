# Generated by Django 4.2.18 on 2025-03-19 15:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carbon_footprint_categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=123)),
                ('co2_emission_kg', models.DecimalField(decimal_places=2, max_digits=10)),
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
                ('carbon_footprint_category', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='RepairCafe.carbon_footprint_categories')),
                ('customer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='RepairCafe.customer')),
                ('queue', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='RepairCafe.queue')),
                ('repairer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='RepairCafe.repairer')),
            ],
        ),
    ]
