from django import forms
from accounts.models import Profile

class ProfileUpdatePanelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','image','national_id', 'phone_number', 'address', 'postal_code']

from django import forms
from orders.models import Request  # مدل خود را وارد کنید

class RequestUpdateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = '__all__'  # لیست فیلدهایی که می‌خواهید در فرم نمایش داده شوند
