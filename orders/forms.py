# forms.py

from django import forms
from .models import RequestInfo, SampleInfo, Request, ExperimentInfo, AdditionalInfo, DiscountInfo

class RequestInfoForm(forms.ModelForm):
    class Meta:
        model = RequestInfo
        fields = ['experiment', 'description']  # حذف فیلد user

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RequestInfoForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(RequestInfoForm, self).save(commit=False)
        instance.user = self.user  # تنظیم کاربر به کاربر جاری
        if commit:
            instance.save()
        return instance

class SampleInfoForm(forms.ModelForm):
    class Meta:
        model = SampleInfo
        fields = ['sample_type', 'sample_amount', 'sample_unit', 'additional_info', 
                  'is_perishable', 'expiration_date', 'sample_return', 
                  'storage_duration', 'storage_unit']

class ExperimentInfoForm(forms.ModelForm):
    class Meta:
        model = ExperimentInfo
        fields = '__all__'  # Replace with specific fields if necessary

class AdditionalInfoForm(forms.ModelForm):
    class Meta:
        model = AdditionalInfo
        fields = '__all__'  # Replace with specific fields if necessary

class DiscountInfoForm(forms.ModelForm):
    class Meta:
        model = DiscountInfo
        fields = ['is_faculty_member', 'is_student_or_staff', 
                  'is_affiliated_with_institution', 'discount_institution_name']