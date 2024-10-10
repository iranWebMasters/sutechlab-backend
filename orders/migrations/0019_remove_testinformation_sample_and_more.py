# Generated by Django 5.0.4 on 2024-10-09 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_testinformation_parameter_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testinformation',
            name='sample',
        ),
        migrations.AddField(
            model_name='testinformation',
            name='user_sample',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.sampleinfo', verbose_name='شناسه نمونه آزمایش'),
            preserve_default=False,
        ),
    ]