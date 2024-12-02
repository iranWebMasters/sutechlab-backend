# Generated by Django 5.0.4 on 2024-10-11 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_request_experiment_alter_request_discountinfo'),
        ('services', '0028_alter_parameters_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='requestinfo',
            new_name='request_info',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='testinfo',
            new_name='test_info',
        ),
        migrations.RemoveField(
            model_name='request',
            name='discountInfo',
        ),
        migrations.AddField(
            model_name='request',
            name='discount_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.discountinfo', verbose_name='اطلاعات تخفیف'),
        ),
        migrations.AlterField(
            model_name='request',
            name='experiment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.experiment', verbose_name='آزمایش'),
        ),
    ]