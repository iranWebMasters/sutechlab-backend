# Generated by Django 5.0.4 on 2024-10-10 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_rename_testinformation_testinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='experimentinfo',
        ),
        migrations.AddField(
            model_name='request',
            name='testinfo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.testinfo', verbose_name='اطلاعات آزمایش'),
        ),
        migrations.DeleteModel(
            name='ExperimentInfo',
        ),
    ]
