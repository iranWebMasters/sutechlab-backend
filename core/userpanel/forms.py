from django import forms
from accounts.models import Profile
from orders.models import Order 


class ProfileUpdatePanelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','image','national_id', 'phone_number', 'address', 'postal_code']

class RequestUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class PaymentForm(forms.Form):
    use_wallet = forms.BooleanField(required=False, label='از کیف پول استفاده شود')
