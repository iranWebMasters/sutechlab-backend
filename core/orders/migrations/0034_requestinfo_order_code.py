# Generated by Django 5.0.4 on 2024-10-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0033_alter_laboratoryrequest_customer_sample_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestinfo',
            name='order_code',
            field=models.CharField(blank=True, max_length=255, unique=True, verbose_name='کد سفارش'),
        ),
    ]