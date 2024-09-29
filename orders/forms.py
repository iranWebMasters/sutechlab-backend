from django import forms
from django.forms import modelformset_factory
from .models import *

class RequestInfoForm(forms.ModelForm):
    class Meta:
        model = RequestInfo
        fields = ['description']  # فقط فیلد توضیحات را وارد می‌کنیم
class SampleInfoForm(forms.ModelForm):
    class Meta:
        model = SampleInfo
        fields = '__all__'
        # fields = ['sample_type', 'sample_amount', 'sample_unit', 'additional_info', 'is_perishable', 'expiration_date', 'sample_return', 'storage_duration', 'storage_unit']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'storage_duration': forms.NumberInput(attrs={'min': 0}),
        }

SampleInfoFormSet = modelformset_factory(
    SampleInfo,
    form=SampleInfoForm,
    extra=3,  # تعداد فرم‌های خالی اضافی که نمایش داده می‌شود
    can_delete=True  # امکان حذف فرم‌ها توسط کاربر
)