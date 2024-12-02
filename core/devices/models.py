from django.db import models

class Device(models.Model):
    name = models.CharField("نام دستگاه", max_length=255)
    brand = models.CharField("برند", max_length=255)
    usage = models.CharField("کاربرد", max_length=255)
    services_description = models.TextField("شرح خدمات")
    additional_details = models.TextField("توضیحات", blank=True, null=True)
    image = models.ImageField("تصویر", upload_to='services_images/')
    status = models.BooleanField("وضعیت", default=False)
    
    class Meta:
        ordering = ['brand']
        verbose_name = "دستگاه"
        verbose_name_plural = "دستگاه ها"

    def __str__(self):
        return "{} - {}".format(self.brand, self.id)
