# Generated by Django 5.0.4 on 2024-09-05 10:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_experiment_parameters_alter_experiment_operator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='faculty',
        ),
        migrations.AddField(
            model_name='laboratory',
            name='faculty',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, related_name='experiments', to='services.faculty', verbose_name='دانشکده'),
            preserve_default=False,
        ),
    ]
