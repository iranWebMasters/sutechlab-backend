from django.db import models

class Device(models.Model):
    STATUS_CHOICES = (
        ('ready', 'آماده سرویس دهی'),
        ('in_progress', 'در حال راه اندازی'),
        ('out_of_service', 'خارج از سرویس'),
    )

    DISPLAY_CHOICES = (
        ('show', 'نمایش در صفحه اصلی'),
        ('hide', 'عدم نمایش در صفحه اصلی'),
    )

    name = models.CharField("نام دستگاه", max_length=255)
    english_name = models.CharField("نام انگلیسی دستگاه", max_length=255, blank=True, null=True)
    model = models.CharField("مدل دستگاه", max_length=255)
    usage = models.CharField("کاربرد", max_length=255, blank=True, null=True)
    manufacturer = models.CharField("شرکت سازنده", max_length=255, blank=True, null=True)
    country = models.CharField("کشور سازنده", max_length=255, blank=True, null=True)
    services_description = models.TextField("شرح خدمات", blank=True, null=True)
    additional_details = models.TextField("توضیحات", blank=True, null=True)
    image = models.ImageField("تصویر", upload_to='services_images/')
    status = models.CharField("وضعیت", max_length=20, choices=STATUS_CHOICES, default='ready')
    
    display_option = models.CharField("گزینه نمایش",max_length=4,choices=DISPLAY_CHOICES,default='show')

    class Meta:
        ordering = ['model']
        verbose_name = "دستگاه"
        verbose_name_plural = "دستگاه ها"

    def get_status_display(self):
        status_dict = dict(self.STATUS_CHOICES)
        return status_dict.get(self.status, 'نامشخص')

    def __str__(self):
        status_dict = dict(self.STATUS_CHOICES)
        status_display = status_dict.get(self.status, 'نامشخص')
        return f"{self.name} (نام انگلیسی: {self.english_name or 'نامشخص'}, مدل: {self.model}, شناسه: {self.id}, وضعیت: {status_display}, سازنده: {self.manufacturer or 'نامشخص'}, کشور: {self.country or 'نامشخص'})"