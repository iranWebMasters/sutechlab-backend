from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django_jalali.db import models as jmodels
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField("نام", max_length=31)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

class Post(models.Model):
    title = models.CharField("عنوان", max_length=255)
    content = RichTextField("محتوا")
    tags = TaggableManager("برچسب‌ها")
    published_date = jmodels.jDateField("تاریخ انتشار", null=True)
    status = models.BooleanField("نمایش در سایت", default=True)
    created_date = jmodels.jDateField("تاریخ ایجاد", auto_now_add=True)
    updated_date = jmodels.jDateField("تاریخ بروزرسانی", auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="نویسنده")
    counted_views = models.IntegerField("تعداد بازدیدها", default=0)
    counted_comment = models.IntegerField("تعداد نظرات", default=0)
    category = models.ManyToManyField(Category, verbose_name="دسته‌بندی")
    image = models.ImageField("تصویر", upload_to='post_images/') 

    class Meta:
        ordering = ['-created_date']
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"

    def __str__(self):
        return "{}-{}".format(self.title, self.id)
    
    def get_absolute_url(self):
        return reverse('blog:single', kwargs={'pid': self.id})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="پست")
    name = models.CharField("نام", max_length=100)
    email = models.EmailField("ایمیل")
    phone_number = models.CharField("شماره تلفن", max_length=200)
    message = models.TextField("پیام")
    approved = models.BooleanField("تایید شده", default=False)
    created_date = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_date = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f'{self.name} - {self.phone_number}'
