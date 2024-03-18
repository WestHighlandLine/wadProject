from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile, Group, Comment, Post, PostReport, UserReport
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
    profile_picture = forms.ImageField()
    biography = forms.CharField(max_length=100, required=False)

    class Meta:
        model = UserProfile
        fields = ('profile_picture','biography',)



class GroupForm(forms.ModelForm):

    name = forms.CharField()
    owner = forms.CharField()
    is_private = forms.BooleanField()
    about = forms.CharField()

    class Meta: 
        model = Group
        fields = ('name', 'owner', 'is_private', 'about',)



class PostForm(forms.ModelForm):
    caption = forms.CharField(label='Caption', max_length=255)
    photo = forms.ImageField(label='Photo')
    latitude = forms.DecimalField(label="Latitude")
    longitude = forms.DecimalField(label="Longitude")

    class Meta:
        model = Post
        fields = ("caption", "photo", "latitude", "longitude",)



class CommentForm(forms.ModelForm):

    commenter = forms.ModelChoiceField(queryset=User.objects.all(), label='Commenter')
    time = forms.DateTimeField(label='Time')
    class Meta: 
        model = Comment
        fields = ('commenter', 'post', 'comment', 'time', )



class ReportForm(forms.ModelForm):

    reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'custom-textarea', 'rows': 5}), label='Reason')

    class Meta: 
        model = PostReport
        fields = ('reason',)



class UserReportForm(forms.ModelForm):

    reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'custom-textarea', 'rows': 5}), label='Reason')

    class Meta: 
        model = UserReport
        fields = ('reason',)
    


class CustomPasswordChangeForm(PasswordChangeForm):
    pass

class ChangePost(forms.ModelForm):

    caption = forms.CharField(label='Caption', max_length=255)
    photo = forms.ImageField(label='Photo')
    
    class Meta:
        model = Post
        fields = ('caption', 'photo', 'latitude', 'longitude',)
    
    def clean(self):
        cleaned_data = super(self).clean()
        return cleaned_data


