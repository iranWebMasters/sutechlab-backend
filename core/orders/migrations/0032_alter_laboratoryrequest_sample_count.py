# Generated by Django 5.0.4 on 2024-10-12 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0031_laboratoryrequest_invoice_pdf_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='sample_count',
            field=models.PositiveIntegerField(null=True, verbose_name='تعداد نمونه'),
        ),
    ]
