# Generated by Django 5.1.1 on 2025-01-27 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hyperlink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='logos/')),
                ('url', models.URLField()),
            ],
        ),
    ]
