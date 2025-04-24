# forms.py
from django import forms


class TestSearchForm(forms.Form):
    test_name = forms.CharField(required=False, label="نام آزمون")
    laboratory_name = forms.CharField(required=False, label="نام آزمایشگاه")
    faculty_name = forms.CharField(required=False, label="نام دانشکده")
