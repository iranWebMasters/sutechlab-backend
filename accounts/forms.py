from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False,help_text="لطفا یک ایمیل معتبر وارد کنید.")
    
    class Meta:
        model = User
        fields = ('email','password1','password2')
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['password1'].help_text = 'رمز عبور باید حداقل 8 کاراکتر باشد.'
            self.fields['password2'].help_text = 'تکرار گذرواژه باید مشابه گذرواژه اصلی باشد.'