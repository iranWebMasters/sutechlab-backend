# Generated by Django 5.0.4 on 2024-09-05 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_experimentspecification_remove_experiment_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='description',
        ),
    ]