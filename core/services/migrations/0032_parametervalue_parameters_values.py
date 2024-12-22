# Generated by Django 5.1.1 on 2024-12-22 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0031_remove_parameters_laboratory"),
    ]

    operations = [
        migrations.CreateModel(
            name="ParameterValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=255, verbose_name="مقدار")),
            ],
            options={
                "verbose_name": "مقدار پارامتر",
                "verbose_name_plural": "مقادیر پارامترها",
            },
        ),
        migrations.AddField(
            model_name="parameters",
            name="values",
            field=models.ManyToManyField(
                related_name="parameters",
                to="services.parametervalue",
                verbose_name="مقادیر",
            ),
        ),
    ]
