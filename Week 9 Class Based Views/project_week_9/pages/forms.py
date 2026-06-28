from django import forms
from django.contrib.auth.models import User
from .models import Game


class UserForm(forms.ModelForm):

    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-input",
        "placeholder": "Confirm you password"
    }), label="Confirm password")

    class Meta:
        model = User

        fields = ["username", "email", "password"]

        labels = {
            "username": "Username",
            "email": "Email",
            "password": "Password"
        }

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-input", "placeholder": "Enter Username"}),
            "email": forms.EmailInput(attrs={"class": "form-input", "placeholder": "Enter Email"}),
            "password": forms.PasswordInput(attrs={"class": "form-input", "placeholder": "Enter Password"})
        }

    def clean_password(self):
        password = self.cleaned_data["password"]

        numbers_contain = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char in numbers_contain for char in password):
            raise forms.ValidationError("Password must contain at least one number.")
        
        return password
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already token.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    

class GameForm(forms.ModelForm):

    class Meta:
        model = Game

        fields = ["title", "description", "platform", "hours_played", "status", "rating"]

        labels = {
            "title": "Game Title",
            "description": "Game Description",
            "platform": "Main Platform",
            "hours_played": "Hours Played",
            "status": "Status",
            "rating": "Rating"
        }

        help_texts = {
            "platform": "Main platform the game is made for, if 2 or more, choose main 1.",
            "hours_played": "If you never played it, leave 0."
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter Title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Describe your game ...",
                "rows": 4
            }),
            "platform": forms.Select(
                choices=[("playstation", "Playstation"), ("nintendo", "Nintendo"), ("xbox", "Xbox"), ("pc", "PC"), ("steam", "Steam")],
                attrs={"class": "form-input"}
            ),
            "hours_played": forms.NumberInput(attrs={"class": "form-input"}),
            "status": forms.Select(
                choices=[("want", "Want to Play"), ("playing", "Playing"), ("finished", "Finished"), ("dropped", "Dropped")],
                attrs={"class": "form-input"}
            ),
            "rating": forms.Select(
                choices=[
                    (1, "1 - Shit"),
                    (2, "2 - Shit with flower"),
                    (3, "3 - Can spend 1 hour"),
                    (4, "4 - CS Go Level"),
                    (5, "5 - No Bad"),
                    (6, "6 - Normal"),
                    (7, "7 - Good"),
                    (8, "8 - You Need to Play"),
                    (9, "9 - Amazing"),
                    (10, "10 - Unique"),
                    ],
                attrs={"class": "form-input"}
            )
        }
    def clean_description(self):
        description = self.cleaned_data["description"]
        #Down is oka but better up for 1 clean
        #note = self.cleaned_data.get("note")

        if description and len(description) > 500 or len(description) < 50:
            raise forms.ValidationError(
                "Note must be between 50 - 500 characters."
            )
        
        return description
    
    def clean_title(self):
        title = self.cleaned_data["title"]

        qs = Game.objects.filter(title__iexact=title)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Title is already taken.")
        return title
    
    