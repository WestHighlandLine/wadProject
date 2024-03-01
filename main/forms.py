from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)




class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField() 

    class Meta:
        model = UserProfile
        fields = ('picture',)
        

class CustomPasswordChangeForm(PasswordChangeForm):
    pass
    
    
    

