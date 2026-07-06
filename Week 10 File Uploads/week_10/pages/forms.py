from django import forms 
from django.contrib.auth.models import User
from .models import BlogPost, Profile


class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-input",
        "placeholder": "Confirm Password"
    }), label="Confirm Password")

    class Meta:
        model = User

        fields = ["username", "email", "password"]

        labels = {
            "username": "Username",
            "email": "Email",
            "password": "Password"
        }

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-input", "placeholder": "Enter username"}),
            "email": forms.EmailInput(attrs={"class": "form-input", "placeholder": "Enter Email"}),
            "password": forms.PasswordInput(attrs={"class": "form-input", "placeholder": "Enter password"})
        }
    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username is already taken."
            )
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_conf = cleaned_data.get("password_confirm")

        if password and password_conf and password_conf != password:
            raise forms.ValidationError(
                "Passwords do not match."
            )
        return cleaned_data
    
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost

        fields = ["title", "content", "cover_image"]

        labels = {
            "title": "Title",
            "content": "Content",
            "cover_image": "Cover Image"
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter Title"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Write you blog post..."
            }),
            "cover_image": forms.ClearableFileInput(attrs={
                "class": "form-input",
                "accept": ".JPG, .jpeg, .png, .webp, .heic, .heif",
                "multiple": False,
                "required": False
            })
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]

        widgets = {
            "avatar": forms.ClearableFileInput(attrs={
                "class": "form-input",
                "accept": ".jpg, .jpeg, .png, .webo, .heic, .heif"
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-input",
                "rows": 4,
                "placeholder": "Write something about yourself..."
            })
        }

