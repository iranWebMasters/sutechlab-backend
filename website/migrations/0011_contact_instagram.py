# Generated by Django 4.2 on 2024-05-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_alter_aboutus_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='instagram',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='آدرس Instagram'),
        ),
    ]
