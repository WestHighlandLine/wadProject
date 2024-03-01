from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )


class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField() 

    class Meta:
        model = UserProfile
        fields = ('picture',)
        

class CustomPasswordChangeForm(PasswordChangeForm):
    pass
    
    
    

