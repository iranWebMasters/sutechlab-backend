# Generated by Django 5.1.1 on 2024-12-22 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0033_parametervalue_max_value_parametervalue_min_value_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="parametervalue",
            name="value",
            field=models.CharField(max_length=255, verbose_name="مقدار پیش فرض"),
        ),
    ]
