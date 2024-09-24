# Generated by Django 5.0.4 on 2024-09-24 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0021_rename_unit_amount_unitamount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='standards',
        ),
        migrations.AddField(
            model_name='test',
            name='parameters',
            field=models.ManyToManyField(related_name='standards', to='services.parameters', verbose_name='پارامترها'),
        ),
        migrations.DeleteModel(
            name='Standards',
        ),
    ]
