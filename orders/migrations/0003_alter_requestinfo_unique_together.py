# Generated by Django 5.0.4 on 2024-09-24 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_user'),
        ('orders', '0002_remove_experimentinfo_cost_and_more'),
        ('services', '0025_remove_test_unit_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='requestinfo',
            unique_together={('user', 'experiment')},
        ),
    ]