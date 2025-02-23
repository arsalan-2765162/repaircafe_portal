# Generated by Django 4.2.11 on 2025-02-11 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RepairCafe', '0003_auto_20250121_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='repairStatus',
            field=models.CharField(choices=[('WAITING', 'Waiting'), ('WAITING_TO_JOIN', 'Waiting to Join Queue'), ('COMPLETED', 'Completed'), ('NEED_PAT', 'Needs PAT tested'), ('INCOMPLETE', 'Incomplete'), ('BEING_REPAIRED', 'Currently being Repaired'), ('PAT_TESTING', 'Currently being PAT tested'), ('PAT_PASSED', 'PAT Test Passed'), ('PAT_FAILED', 'PAT Test Failed')], default='WAITING_TO_JOIN', max_length=128),
        ),
    ]
