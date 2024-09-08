from django import forms
from .models import Request,Sample

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['user', 'request_type', 'description']  # فیلدهای مورد نیاز را مشخص کنید
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),  # تنظیمات ظاهری برای فیلد توضیحات
        }

from django import forms
from .models import Sample

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['request', 'sample_type', 'sample_amount', 'sample_unit', 'additional_info', 'is_perishable', 'expiration_date', 'storage_duration', 'storage_unit']  # فیلدهای مورد نیاز را مشخص کنید
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': 4, 'cols': 15}),  # تنظیمات ظاهری برای فیلد توضیحات اضافی
        }