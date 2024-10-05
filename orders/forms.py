from django import forms
from django.forms import modelformset_factory
from .models import  RequestInfo,SampleInfo

class RequestInfoForm(forms.ModelForm):
    class Meta:
        model = RequestInfo
        fields = ['description']
        
class RequestInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = RequestInfo
        fields = ['description']


class SampleForm(forms.ModelForm):
    class Meta:
        model = SampleInfo
        fields = [
            'sample_type',
            'customer_sample_name',
            'sample_count',
            'is_perishable',
            'expiration_date',
            'storage_duration',
            'storage_duration_unit',
            'sample_description',
            'storage_conditions',
            'file_upload'
        ]
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sample_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'storage_conditions': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'file_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'sample_type': 'نوع نمونه',
            'customer_sample_name': 'نام نمونه مشتری',
            'sample_count': 'تعداد نمونه',
            'is_perishable': 'نمونه فاسدشدنی است',
            'expiration_date': 'تاریخ انقضا',
            'storage_duration': 'مدت زمان نگهداری',
            'storage_duration_unit': 'واحد مدت زمان نگهداری',
            'sample_description': 'توضیحات نمونه',
            'storage_conditions': 'شرایط نگهداری',
            'file_upload': 'فایل تکمیلی نمونه',
        }