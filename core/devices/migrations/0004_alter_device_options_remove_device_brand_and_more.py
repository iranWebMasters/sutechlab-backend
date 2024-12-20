# Generated by Django 5.1.1 on 2024-12-18 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("devices", "0003_device_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="device",
            options={
                "ordering": ["model"],
                "verbose_name": "دستگاه",
                "verbose_name_plural": "دستگاه ها",
            },
        ),
        migrations.RemoveField(
            model_name="device",
            name="brand",
        ),
        migrations.AddField(
            model_name="device",
            name="country",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="کشور سازنده"
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="english_name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="نام انگلیسی دستگاه"
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="manufacturer",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="شرکت سازنده"
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="model",
            field=models.CharField(
                default=1, max_length=255, verbose_name="مدل دستگاه"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="device",
            name="services_description",
            field=models.TextField(blank=True, null=True, verbose_name="شرح خدمات"),
        ),
        migrations.AlterField(
            model_name="device",
            name="status",
            field=models.CharField(
                choices=[
                    ("ready", "آماده سرویس دهی"),
                    ("in_progress", "در حال راه اندازی"),
                    ("out_of_service", "خارج از سرویس"),
                ],
                default="ready",
                max_length=20,
                verbose_name="وضعیت",
            ),
        ),
    ]