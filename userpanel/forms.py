from django import forms
from accounts.models import Profile

class ProfileUpdatePanelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','image','national_id', 'phone_number', 'address', 'postal_code']