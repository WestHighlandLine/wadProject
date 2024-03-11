from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile, Group, Comment, Post, Report
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

    class Meta:
        model = UserProfile
        fields = ('profile_picture',)



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

    reporter = forms.ModelChoiceField(queryset=User.objects.all(), label='Reporter')
    post_id = forms.ModelChoiceField(queryset=Post.objects.all(), label='Post')
    reason = forms.CharField(widget=forms.Textarea, label='Reason')

    class Meta: 
        model = Report
        fields = ('reporter', 'post_id', 'reason',)



class CustomPasswordChangeForm(PasswordChangeForm):
    
    input_new_password = forms.CharField(
        label="Input New Password",
        widget=forms.PasswordInput(),
    )
    new_password_confirm = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(),
    )
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_confirm = cleaned_data.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise forms.ValidationError("New passwords do not match")
        return cleaned_data

class ChangePost(forms.ModelForm):
    pass

class ChangeInfoForm(forms.ModelForm):
    picture = forms.ImageField() 

    class Meta:
        model = UserProfile
        fields = ('picture',)

