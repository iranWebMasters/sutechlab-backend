from django.db import models
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField("نام", max_length=31)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

class Services(models.Model):
    title = models.CharField("عنوان", max_length=255)
    content = RichTextField("محتوا")
    status = models.BooleanField("وضعیت", default=False)
    published_date = models.DateTimeField("تاریخ انتشار", null=True,auto_now_add=True)
    created_date = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_date = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)
    category = models.ManyToManyField(Category, verbose_name="دسته‌بندی")
    image = models.ImageField("تصویر", upload_to='services_images/') 

    class Meta:
        ordering = ['-created_date']
        verbose_name = "خدمات"
        verbose_name_plural = "خدمات"

    def __str__(self):
        return "{}-{}".format(self.title, self.id)
