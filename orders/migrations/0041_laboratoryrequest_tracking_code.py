# Generated by Django 5.0.4 on 2024-10-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0040_alter_laboratoryrequest_final_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratoryrequest',
            name='tracking_code',
            field=models.CharField(default=1, max_length=255, verbose_name='Tracking Code'),
            preserve_default=False,
        ),
    ]
