# Generated by Django 5.0.4 on 2024-10-12 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0030_laboratoryrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratoryrequest',
            name='invoice_pdf',
            field=models.FileField(blank=True, null=True, upload_to='invoices/', verbose_name='پیش فاکتور'),
        ),
        migrations.AddField(
            model_name='laboratoryrequest',
            name='is_complete',
            field=models.BooleanField(default=False, verbose_name='تکمیل شده'),
        ),
        migrations.AddField(
            model_name='laboratoryrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'در حال بررسی'), ('successful', 'پرداخت موفق'), ('failed', 'پرداخت ناموفق'), ('canceled', 'لغو شده')], default='pending', max_length=20, verbose_name='وضعیت'),
        ),
    ]
