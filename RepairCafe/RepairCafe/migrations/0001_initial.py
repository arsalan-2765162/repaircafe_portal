# Generated by Django 2.2.28 on 2024-11-19 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=128)),
                ('lastName', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Repairer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=128)),
                ('lastName', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('repairNumber', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('itemName', models.CharField(max_length=128)),
                ('itemCategory', models.CharField(choices=[('ELEC', 'Electrical'), ('TEXT', 'Clothing & Textiles'), ('TOOLS', 'tools & equipment')], max_length=128)),
                ('itemDescription', models.CharField(max_length=256)),
                ('repairStatus', models.CharField(choices=[('WAITING', 'Waiting'), ('COMPLETED', 'Completed'), ('NEED_PAT', 'Needs PAT tested'), ('INCOMPLETE', 'Incomplete')], default='WAITING', max_length=128)),
                ('position', models.IntegerField(default=0)),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RepairCafe.Queue')),
            ],
        ),
    ]
