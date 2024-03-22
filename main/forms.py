from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile, Group, Comment, Post, PostReport, UserReport, ContactUs


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise forms.ValidationError("Your password must contain at least 8 characters.")
        
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages[0])
        
        if password.isdigit():
            raise forms.ValidationError("Your password can't be entirely numeric.")

        return password

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField()
    biography = forms.CharField(max_length=100, required=False, label="Biography (optional)")

    class Meta:
        model = UserProfile
        fields = (
            "profile_picture",
            "biography",
        )


class GroupForm(forms.ModelForm):
    name = forms.CharField()
    about = forms.CharField(required=False)

    class Meta:
        model = Group
        fields = (
            "name",
            "about",
        )


class PostForm(forms.ModelForm):
    caption = forms.CharField(label="Caption", max_length=255)
    photo = forms.ImageField(label="Photo")
    group = forms.ModelChoiceField(label="Group (optional)", queryset=None, required=False)
    latitude = forms.DecimalField(label="Latitude")
    longitude = forms.DecimalField(label="Longitude")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["group"].queryset = self.request.user.created_by.groups_members.all()

    class Meta:
        model = Post
        fields = (
            "caption",
            "photo",
            "group",
            "latitude",
            "longitude",
        )


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "comment-textarea",
                "rows": 5,
                "placeholder": "Write a comment...",
            }
        ),
        label="",
    )

    class Meta:
        model = Comment
        fields = ("comment",)


class ReportForm(forms.ModelForm):

    reason = forms.CharField(
        widget=forms.Textarea(attrs={"class": "custom-textarea", "rows": 5}),
        label="Reason",
    )

    class Meta:
        model = PostReport
        fields = ("reason",)


class UserReportForm(forms.ModelForm):

    reason = forms.CharField(
        widget=forms.Textarea(attrs={"class": "custom-textarea", "rows": 5}),
        label="Reason",
    )

    class Meta:
        model = UserReport
        fields = ("reason",)


class ChangePost(forms.ModelForm):

    caption = forms.CharField(label="Caption", max_length=255)
    photo = forms.ImageField(label="Photo")

    class Meta:
        model = Post
        fields = (
            "caption",
            "photo",
            "latitude",
            "longitude",
        )

    def clean(self):
        cleaned_data = super(self).clean()
        return cleaned_data
    
class ContactUsForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your message'}))

    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'subject', 'message',)

