from django import forms
from custom_user.models import CustomUser

class UserForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password']