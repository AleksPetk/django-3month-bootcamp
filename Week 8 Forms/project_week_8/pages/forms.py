from django import forms
from .models import Category, Review
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
            "description"
        ]

        labels = {
            "name": "Category Name",
            "description": "Category Description"
        }

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form_input",
                "placeholder": "Enter Name"
            }),
            "description": forms.Textarea(attrs={
                "class": "form_input",
                "placeholder": "Explain about the category.",
                "rows": 5
            })
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        bad_words = ["fuck", "idiot", "suck", "pussy", "anal", "boobs", "dick"]
        for word in bad_words:
            if word in name.lower():
                raise forms.ValidationError(
                    f"Name cannot contains '{word}'."
                )
        return name
    
    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        if len(description) < 20:
            raise forms.ValidationError(
                "Description should be at least 20 characters."
            )
        return description
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name").strip()
        description = cleaned_data.get("description").strip()
        if name.lower() in description.lower():
            raise forms.ValidationError(
                "Description cannot contains name."
            )
        return cleaned_data
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = [
            "title",
            "category",
            "content",
            "rating",
            "recommended"
        ]

        labels = {
            "title": "TITLE",
            "category": "CATEGORY",
            "content": "CONTENT",
            "rating": "RATING",
            "recommended": "RECOMMENDED"
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "text_input",
                "placeholder": "Enter Title"
            }),
            "category": forms.Select(attrs={
                "class": "text_input"
            }),
            "content": forms.Textarea(attrs={
                "class": "text_input",
                "placeholder": "Explain your review...",
                "rows": 5
            }),
            "rating": forms.NumberInput(attrs={
                "class": "text_input",
                "min": 1,
                "max": 10
            }),
            "recommended": forms.CheckboxInput(attrs={
                "class": "text_input",
            })
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError(
                "Title too short"
            )
        bad_words = ["fuck", "suck", "dick", "pussy", "bad"]
        for word in bad_words:
            if word in title.lower():
                raise forms.ValidationError(
                    f"Title cannot contains '{word}'"
                )
        return title

    def clean_content(self):
        content = self.cleaned_data["content"].strip()
        if len(content) < 20:
            raise forms.ValidationError(
                "Content too short, should be over 20 characters."
            )
        if len(content) > 300:
            raise forms.ValidationError(
                "Content too long, should be under 300 characters."
            )
        return content

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if title and content:
            if title.lower() in content.lower():
                raise forms.ValidationError(
                    "Content cannot contain title."
                )
        return cleaned_data
    
    
class UserForm(forms.ModelForm):

    password_confirm = forms.CharField(
        min_length=8,
        label = "Confirm Password",
        widget = forms.PasswordInput(attrs={
            "class": "form_input",
            "placeholder": "Enter Confirm Password"
        })
    )

    class Meta:
        
        model = User

        fields = [
            "username",
            "password"
        ]

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

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 8:
            raise forms.ValidationError(
                "Password should be at least 8 characters length."
            )
        return password
    
    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if "admin" in username.lower():
            raise forms.ValidationError(
                "Username cannot contains 'admin'."
            )
        
        if len(username) < 3:
            raise forms.ValidationError(
                "Too short, username should be at least 3 characters."
            )
        
        return username
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        username = cleaned_data.get("username")

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(
                    "Passwords do not match."
                )
        if username and password:
            if username.lower() in password.lower() or password.lower() in username.lower():
                raise forms.ValidationError(
                    "Password is too similar to username."
                )
            
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user