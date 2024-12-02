# Generated by Django 5.0.4 on 2024-10-11 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_remove_request_additional_info_request_discountinfo_and_more'),
        ('services', '0028_alter_parameters_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='experiment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='services.experiment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='request',
            name='discountInfo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.discountinfo', verbose_name='اطلاعات '),
        ),
    ]