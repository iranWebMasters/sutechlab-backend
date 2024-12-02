# Generated by Django 5.0.4 on 2024-10-12 11:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0032_alter_laboratoryrequest_sample_count'),
        ('services', '0028_alter_parameters_unit'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='customer_sample_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام نمونه مشتری'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='discount_institution_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام نهاد تخفیف'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='experiment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.experiment', verbose_name='آزمایش'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='is_affiliated_with_institution',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='آیا کاربر متقاضی استفاده از تخفیف نهادهای طرف قرارداد است؟'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='is_complete',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='تکمیل شده'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='is_faculty_member',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='آیا کاربر عضو هیات علمی است؟'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='is_student_or_staff',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='آیا کاربر دانشجو یا کارکنان دانشگاه است؟'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='parameter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.parameters', verbose_name='پارامتر'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='parameter_value',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='مقدار پارامتر'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='repeat_count_test',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد تکرار آزمون'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='sample_count',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد نمونه'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='sample_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='نوع نمونه'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'در حال بررسی'), ('successful', 'پرداخت موفق'), ('failed', 'پرداخت ناموفق'), ('canceled', 'لغو شده')], default='pending', max_length=20, null=True, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='submission_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='تاریخ ثبت درخواست'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='laboratoryrequest',
            name='user_sample',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='شناسه نمونه آزمایش'),
        ),
    ]
