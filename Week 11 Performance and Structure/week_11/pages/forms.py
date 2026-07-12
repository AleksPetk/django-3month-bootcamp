"""Forms used by the pages applications."""

from django import forms
from django.contrib.auth.models import User

from .models import Post, Comment, Car


#----------------------------------------
# Post Form
#----------------------------------------

class PostForm(forms.ModelForm):
    """Create or update a blog post."""

    class Meta:
        model = Post
        fields = ["title", "content", "category", "cover_image", "is_published"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter title"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Write your post...",
                "rows": 5
            }),
            "category": forms.Select(attrs={
                "class": "form-input"
            }),
            "cover_image": forms.ClearableFileInput(attrs={
                "class": "form-input",
                "accept": ".jpg,.jpeg,.png,.webp,.heic,.heif"
            }),
            "is_published": forms.CheckboxInput(attrs={
                "class": "form-checkbox"
            })
        }


#----------------------------------------
# Comment Form
#----------------------------------------

class CommentForm(forms.ModelForm):
    """Create or update a comment."""

    class Meta:
        model = Comment
        fields = ["content"]
        labels = {
            "content": "Content"
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-input",
                "rows": 3,
                "placeholder": "Write a comment..."
            })
        }


#----------------------------------------
# Car Form
#----------------------------------------

class CarForm(forms.ModelForm):
    """Create or update a car."""

    class Meta:
        model = Car
        fields = ["make", "model", "year"]

        widgets = {
            "make": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter make"
            }),
            "model": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter model"
            }),
            "year": forms.NumberInput(attrs={
                "class": "form-input",
                "placeholder": "Enter year"
            })
        }


#----------------------------------------
# User registration Form
#----------------------------------------

class UserForm(forms.ModelForm):
    """Register a user and validate password confirmation."""

    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-input",
        "placeholder": "Enter Password Again"
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
                "class": "form-input",
                "placeholder": "Enter Username"
            }),
            "password": forms.PasswordInput(attrs={
                "class": "form-input",
                "placeholder": "Enter Password"
            })
        }

    def clean_username(self):
        """Reject usernames that arleady belong to another user."""

        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username already exists."
            )   
        return username
    
    def clean(self):
        """Check that the password and confirmation match."""

        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                "Passwords do not match."
            )
        
        return cleaned_data
