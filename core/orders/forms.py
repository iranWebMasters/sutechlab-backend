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
        fields = ['user_sample', 'test', 'repeat_count_test', 'parameter',]


class DiscountInfoForm(forms.ModelForm):
    class Meta:
        model = DiscountInfo
        fields = [
            'is_faculty_member', 
            'is_student_or_staff', 
            'is_affiliated_with_institution', 
            'send_cost',  # New field for sending costs
            'contract_party_file',  # New field for contract party file
            'has_labs_net_grant',  # New field for Labs Network grant
            'labs_net_file',  # New field for Labs Network file
            'has_research_grant',  # New field for research grant
            'research_grant_withdrawal_amount'  # New field for withdrawal amount
        ]