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
    MAX_LENGTH = 128
    username = forms.CharField(max_length=128, help_text = "Username") # Matthew - is it possible to get data from the database and put it into the help text?
    email = forms.EmailField(max_length=128, help_text = "Email")
    
    picture = forms.ImageField() 

    class Meta:
        model = UserProfile
        fields = ('username', 'email','picture',)
        

class CustomPasswordChangeForm(PasswordChangeForm):
    pass
    
    
    

