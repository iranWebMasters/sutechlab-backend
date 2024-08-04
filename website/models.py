from django.db import models

class WorkingHour(models.Model):
    DAY_CHOICES = (
        ('Sat', 'شنبه'),
        ('Sun', 'یکشنبه'),
        ('Mon', 'دوشنبه'),
        ('Tue', 'سه شنبه'),
        ('Wed', 'چهار شنبه'),
        ('Thu', 'پنج شنبه'),
        ('Fri', 'جمعه'),
    )

    start_day = models.CharField(max_length=3, choices=DAY_CHOICES, verbose_name="روز شروع")
    end_day = models.CharField(max_length=3, choices=DAY_CHOICES, verbose_name="روز پایان")
    start_time = models.CharField(max_length=256, verbose_name="زمان شروع")
    end_time = models.CharField(max_length=256, verbose_name="زمان پایان")

    class Meta:
        verbose_name = "ساعات کاری"
        verbose_name_plural = "ساعات کاری"

    def __str__(self):
        start_day_text = dict(self.DAY_CHOICES).get(self.start_day, '')
        end_day_text = dict(self.DAY_CHOICES).get(self.end_day, '')
        return f"{start_day_text} تا {end_day_text} {self.start_time}  الی {self.end_time} "

class Contact(models.Model):
    address = models.CharField(max_length=255, verbose_name="آدرس")
    mobile_phone = models.CharField(max_length=15, verbose_name="تلفن همراه")
    landline_phone = models.CharField(max_length=15, verbose_name="تلفن ثابت")
    email = models.EmailField(verbose_name="ایمیل")
    instagram = models.CharField(max_length=255, verbose_name="instagram ID", blank=True, null=True)
    whatsapp = models.CharField(max_length=255, verbose_name="whatsapp ", blank=True, null=True)
    workingHour = models.ForeignKey(WorkingHour, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ساعت کاری")

    class Meta:
        verbose_name = "اطلاعات تماس"
        verbose_name_plural = "اطلاعات تماس"

    def __str__(self):
        return self.email
    
class ContactUs(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=15, verbose_name="تلفن")
    message = models.TextField(verbose_name="پیام")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ به روزرسانی")

    class Meta:
        ordering = ('created_date',)
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    email=models.EmailField(verbose_name="ایمیل")

    class Meta:
        verbose_name = "خبرنامه"
        verbose_name_plural = "خبرنامه‌ها"

    def __str__(self):
        return self.email



class HomePage(models.Model):
    title = models.CharField(max_length=255, verbose_name="تیتر صفحه اصلی")
    top_text = models.TextField(verbose_name="متن بالای صفحه")
    banner = models.ImageField(upload_to='banners/', verbose_name="بنر صفحه اصلی")
    aboutـtitle = models.CharField(max_length=255, verbose_name="تیتر  درباره ما صفحه اصلی")
    about_text = models.TextField(verbose_name=" متن درباره صفحه اصلی" )
    aboutـbanner = models.ImageField(upload_to='banners/', verbose_name=" بنر در باره ما صفحه اصلی")
    bottom_text = models.TextField(verbose_name="متن پایین صفحه")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "صفحه اصلی"
        verbose_name_plural = "صفحه اصلی"


class AboutUs(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    aboutuspage_image = models.ImageField(upload_to='aboutus/', verbose_name='تصویر صفحه درباره ما ', blank=True, null=True)
    content = models.TextField(verbose_name='محتوا')

    def __str__(self):
        return f"About Us - {self.title}"

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'صفحه درباره ما'