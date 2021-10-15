from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from . import models

# Register your models here.

# CITATION - https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#a-full-example
# Basically just copy/pasted from the Custom User Assessment

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = models.CustomUser
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Entered Passwords do not Match!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.CustomUser
        fields = ('__all__')

    def clean_password(self):
        return self.initial["password"]


# CITATION - https://stackoverflow.com/questions/48011275/custom-user-model-fields-abstractuser-not-showing-in-django-admin


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {
            'fields': (
                'library_card_number',
                'checked_out_books',
                'reserved_books',
                'profile_image'
            )
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets


admin.site.register(models.CustomUser, UserAdmin)
