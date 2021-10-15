from django import forms
from custom_user.models import CustomUser


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    profile_image = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = ['username']
