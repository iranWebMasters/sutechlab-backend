# Generated by Django 5.0.4 on 2024-09-01 14:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_description_profile_address_and_more'),
        ('userpanel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institutes', to='accounts.profile'),
        ),
    ]