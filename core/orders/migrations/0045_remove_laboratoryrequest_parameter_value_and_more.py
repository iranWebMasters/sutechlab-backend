# Generated by Django 5.1.1 on 2024-12-23 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0044_alter_testinfo_parameter_values"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="laboratoryrequest",
            name="parameter_value",
        ),
        migrations.AddField(
            model_name="laboratoryrequest",
            name="parameter_values",
            field=models.JSONField(default=1, verbose_name="مقادیر پارامتر"),
            preserve_default=False,
        ),
    ]