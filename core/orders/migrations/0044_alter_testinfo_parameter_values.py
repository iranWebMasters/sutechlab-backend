# Generated by Django 5.1.1 on 2024-12-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0043_alter_testinfo_parameter_values"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testinfo",
            name="parameter_values",
            field=models.JSONField(default=1, verbose_name="مقادیر پارامتر"),
            preserve_default=False,
        ),
    ]
