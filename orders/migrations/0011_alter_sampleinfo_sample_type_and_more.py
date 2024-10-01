# Generated by Django 5.0.4 on 2024-09-30 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_sampleinfo_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleinfo',
            name='sample_type',
            field=models.CharField(max_length=50, verbose_name='نوع نمونه'),
        ),
        migrations.AlterField(
            model_name='sampleinfo',
            name='sample_unit',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='واحد اندازه\u200cگیری'),
        ),
    ]