from django import forms
from django.contrib.auth.models import User
from .models import DevBlog

class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form_input",
        "placeholder": "Enter password again"
    }), label="Confirm Password")
    class Meta:
        model = User

        fields = ["username", "password"]

        labels = {
            "username": "Username",
            "password": "Password"
        }

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form_input",
                "placeholder": "Enter Username"
            }),
            "password": forms.PasswordInput(attrs={
                "class": "form_input",
                "placeholder": "Enter Password"
            })
        }
    def clean_username(self):
        username = self.cleaned_data["username"]
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username already taken."
            )
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password_confirm != password:
            raise forms.ValidationError(
                "Passwords do not match."
            )
        
        return cleaned_data

class DevBlogForm(forms.ModelForm):
    class Meta:
        model = DevBlog
        fields = ["title", "content", "category", "cover_image"]
        labels = {
            "title": "Title",
            "content": "Content",
            "category": "Category",
            "cover_image": "Cover Image"
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form_input",
                "placeholder": "Enter title"
            }),
            "content": forms.Textarea(attrs={
                "class": "form_input",
                "placeholder": "Type your content here...",
                "rows": 5
            }),
            "category": forms.Select(attrs={
                "class": "form_input",
            }),
            "cover_image": forms.ClearableFileInput(attrs={
                "class": "form_input",
                "accept": ".jpg, .jpeg, .webp, .png, .heic, .heif",
                "multiple": False,
                "required": False
            })
        }