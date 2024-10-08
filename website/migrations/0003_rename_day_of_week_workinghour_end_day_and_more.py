# Generated by Django 4.2 on 2024-04-28 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_workinghour_contact_workinghour'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workinghour',
            old_name='day_of_week',
            new_name='end_day',
        ),
        migrations.AddField(
            model_name='workinghour',
            name='start_day',
            field=models.CharField(choices=[('Sat', 'شنبه'), ('Sun', 'یکشنبه'), ('Mon', 'دوشنبه'), ('Tue', 'سه شنبه'), ('Wed', 'چهار شنبه'), ('Thu', 'پنج شنبه'), ('Fri', 'جمعه')], default=1, max_length=3),
            preserve_default=False,
        ),
    ]
