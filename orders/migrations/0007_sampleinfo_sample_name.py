# Generated by Django 5.0.4 on 2024-09-30 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_requestinfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleinfo',
            name='sample_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام نمونه مشتری'),
        ),
    ]