# Generated by Django 5.0.4 on 2024-10-11 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_discountinfo_experiment_discountinfo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='additional_info',
        ),
        migrations.AddField(
            model_name='request',
            name='discountInfo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.discountinfo', verbose_name='اطلاعات تکمیلی'),
        ),
        migrations.DeleteModel(
            name='AdditionalInfo',
        ),
    ]