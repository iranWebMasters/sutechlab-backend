from django.db import models
from accounts.models import Profile
from devices.models import Device


class UnitAmount(models.Model):
    amount = models.CharField(max_length=50, verbose_name="مقدار")
    unit = models.CharField(max_length=50, verbose_name="واحد اندازه‌گیری")

    def __str__(self):
        return f"{self.amount} {self.unit}"

    class Meta:
        verbose_name = "مقدار واحد"
        verbose_name_plural = "مقادیر واحد"


class UnitPrice(models.Model):
    CURRENCY_CHOICES = [
        ("IRR", "ریال"),
        ("Toman", "تومان"),
    ]

    unit_price = models.DecimalField(
        max_digits=15, decimal_places=0, verbose_name="مبلغ واحد"
    )
    currency = models.CharField(
        max_length=5, choices=CURRENCY_CHOICES, default="IRR", verbose_name="واحد پول"
    )

    def __str__(self):
        return f"{self.unit_price} {self.get_currency_display()}"

    class Meta:
        verbose_name = "قیمت واحد"
        verbose_name_plural = "قیمت‌های واحد"


class Parameters(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام پارامتر")
    unit = models.CharField(max_length=50, verbose_name="واحد اندازه‌گیری")
    unit_amount = models.ForeignKey(
        "UnitAmount",
        on_delete=models.CASCADE,
        related_name="parameters",
        verbose_name="مقدار واحد",
    )
    unit_price = models.ForeignKey(
        "UnitPrice",
        on_delete=models.CASCADE,
        related_name="parameters",
        verbose_name="مبلغ واحد",
    )

    values = models.ManyToManyField(
        "ParameterValue", related_name="parameters", verbose_name="مقادیر"
    )

    def __str__(self):
        return f"{self.name} - {self.unit_amount} - {self.unit} - {self.unit_price}"

    class Meta:
        verbose_name = "پارامتر"
        verbose_name_plural = "پارامترها"


class ParameterValue(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام مقدار")
    default_value = models.CharField(max_length=255, verbose_name="مقدار پیش فرض")
    min_value = models.FloatField(verbose_name="حداقل مقدار", null=True, blank=True)
    max_value = models.FloatField(verbose_name="حداکثر مقدار", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "مقدار پارامتر"
        verbose_name_plural = "مقادیر پارامترها"


class Laboratory(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام آزمایشگاه")
    faculty = models.ForeignKey(
        "Faculty",
        on_delete=models.CASCADE,
        related_name="experiments",
        verbose_name="دانشکده",
        null=True,
        blank=True,
    )
    technical_manager = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="managed_laboratories",
        verbose_name="مدیر فنی",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "آزمایشگاه"
        verbose_name_plural = "آزمایشگاه‌ها"


class Faculty(models.Model):
    LOCATION_CHOICES = [
        ("SD", "صدرا"),
        ("SH", "شیراز"),
    ]
    name = models.CharField(max_length=255, verbose_name="نام دانشکده")
    location = models.CharField(
        max_length=2, choices=LOCATION_CHOICES, verbose_name="مکان"
    )

    def __str__(self):
        return f"{self.name} ({self.get_location_display()})"

    class Meta:
        verbose_name = "دانشکده"
        verbose_name_plural = "دانشکده‌ها"


class Test(models.Model):
    name_fa = models.CharField(max_length=255, verbose_name="نام فارسی آزمون")
    name_en = models.CharField(
        max_length=255, verbose_name="نام انگلیسی آزمون", null=True, blank=True
    )
    operating_range = models.TextField(verbose_name="گستره کاری", null=True, blank=True)
    description = models.TextField(verbose_name="توصیف آزمون", null=True, blank=True)
    parameters = models.ManyToManyField(
        "Parameters", related_name="standards", verbose_name="پارامترها"
    )

    def __str__(self):
        return f"{self.name_fa} / {self.name_en}"

    class Meta:
        verbose_name = "آزمون"
        verbose_name_plural = "آزمون‌ها"


class Sample(models.Model):
    type = models.CharField(max_length=100, verbose_name="نوع نمونه")
    description = models.TextField(verbose_name="توصیف نمونه", blank=True, null=True)
    is_returnable = models.BooleanField(
        default=False, verbose_name="نمونه برگشت پذیر است؟"
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "نمونه"
        verbose_name_plural = "نمونه‌ها"


class Experiment(models.Model):
    STATUS_CHOICES = [
        ("active", "فعال"),
        ("inactive", "غیرفعال"),
    ]
    ISO_CHOICES = [
        ("has", "دارد"),
        ("has_not", "ندارد"),
    ]
    test_name = models.CharField(max_length=255, verbose_name="نام آزمون")
    laboratory = models.ForeignKey(
        "Laboratory",
        on_delete=models.CASCADE,
        related_name="experiments",
        verbose_name="آزمایشگاه",
    )
    tests = models.ManyToManyField(Test, related_name="samples", verbose_name="آزمون‌ها")
    samples = models.ManyToManyField(
        Sample, related_name="experiments", verbose_name="نمونه‌ها"
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="experiments",
        verbose_name="دستگاه",
    )
    operator = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="experiments",
        verbose_name="اپراتور",
    )
    iso_17025 = models.CharField(
        max_length=7, choices=ISO_CHOICES, default="has_not", verbose_name="ISO 17025"
    )
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default="active", verbose_name="وضعیت"
    )
    created_date = models.DateField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_date = models.DateField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    def __str__(self):
        return self.test_name

    def duplicate_experiments(self):
        new_experiment = Experiment.objects.create(
            test_name=self.test_name,
            laboratory=self.laboratory,
            device=self.device,
            operator=self.operator,
            iso_17025=self.iso_17025,
            status=self.status,
            created_date=self.created_date,
            updated_date=self.updated_date,
        )

        new_experiment.tests.set(self.tests.all())
        new_experiment.samples.set(self.samples.all())

        return new_experiment

    class Meta:
        verbose_name = "آزمایش"
        verbose_name_plural = "آزمایش‌ها"
