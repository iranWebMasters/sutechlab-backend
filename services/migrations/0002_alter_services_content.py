# Generated by Django 5.0.4 on 2024-05-07 08:12

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='محتوا'),
        ),
    ]
