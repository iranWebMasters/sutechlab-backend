from django import forms
from .models import Comment  # Import the Comment model from your models.py

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Specify the model to use for the form
        fields = ['name', 'email', 'phone_number', 'message']  # Define the fields to include in the for