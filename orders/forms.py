from django import forms
from .models import  RequestInfo,SampleInfo,TestInfo,DiscountInfo

class RequestInfoForm(forms.ModelForm):
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

class TestInfoForm(forms.ModelForm):
    class Meta:
        model = TestInfo
        fields = ['user_sample', 'test', 'repeat_count_test', 'parameter', 'parameter_value']  # حذف فیلدهای user و experiment
        widgets = {
            'sample': forms.Select(attrs={'class': 'form-control'}),
            'test': forms.Select(attrs={'class': 'form-control'}),
            'repeat_count_test': forms.NumberInput(attrs={'class': 'form-control'}),
            'parameter': forms.Select(attrs={'class': 'form-control'}),
            'parameter_value': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DiscountInfoForm(forms.ModelForm):
    class Meta:
        model = DiscountInfo
        fields = ['is_faculty_member', 'is_student_or_staff', 'is_affiliated_with_institution', 'discount_institution_name']
        widgets = {
            'is_faculty_member': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_student_or_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_affiliated_with_institution': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'discount_institution_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
