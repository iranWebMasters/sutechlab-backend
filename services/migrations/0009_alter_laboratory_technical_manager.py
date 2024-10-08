# Generated by Django 5.0.4 on 2024-09-05 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_image'),
        ('services', '0008_laboratory_technical_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratory',
            name='technical_manager',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='managed_laboratories', to='accounts.profile', verbose_name=' مدیر فنی'),
            preserve_default=False,
        ),
    ]
