# Generated by Django 5.1.1 on 2024-12-22 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0028_alter_parameters_unit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="laboratory",
            name="faculty",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="experiments",
                to="services.faculty",
                verbose_name="دانشکده",
            ),
        ),
        migrations.AlterField(
            model_name="parameters",
            name="laboratory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tests",
                to="services.laboratory",
                verbose_name="آزمایشگاه",
            ),
        ),
        migrations.AlterField(
            model_name="test",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="توصیف آزمون"),
        ),
        migrations.AlterField(
            model_name="test",
            name="name_en",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="نام انگلیسی آزمون"
            ),
        ),
        migrations.AlterField(
            model_name="test",
            name="operating_range",
            field=models.TextField(blank=True, null=True, verbose_name="گستره کاری"),
        ),
    ]
