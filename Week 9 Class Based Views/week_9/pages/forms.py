from django import forms
from .models import Movie, WatchlistItem
from django.contrib.auth.models import User


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie

        fields = [
            "title",
            "description",
            "year",
            "rating",
            "watched",
        ]

        labels = {
            "title": "Movie Title",
            "description": "Movie Description",
            "year": "Release Year",
            "rating": "Movie Rating",
            "watched": "Watched",
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the movie title"
                }),
            "description": forms.Textarea(attrs={
                "class": "form-control", 
                "rows": 5,
                "placeholder": "Enter the movie description"
                }),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control"}),
            "watched": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year < 1950 or year > 2026:
            raise forms.ValidationError("Year must be between 1950 and 2026.")
        return year
    
    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating < 1 or rating > 10:
            raise forms.ValidationError("Rating must be between 1 and 10.")
        return rating
    
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        if Movie.objects.filter(title__iexact=title).exists():
            raise forms.ValidationError("A movie with this title already exists.") 
        return title
    
    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description:
            raise forms.ValidationError("Description cannot be empty.")
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")

        bad_words = ["suck", "stupid", "idiot", "dumb", "hate"]
        if title and description:
            if title.lower() == description.lower():
                raise forms.ValidationError("Title and description cannot be the same.")
        
            for word in bad_words:
                if word in title.lower() or word in description.lower():
                    raise forms.ValidationError(f"Title or description contains inappropriate language: {word}")

        return cleaned_data
    
class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm your password"
        }), label="Confirm Password")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

        labels = {
            "username": "Username",
            "email": "Email Address",
            "password": "Password",
        }

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                }),
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
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data


class WatchlistItemForm(forms.ModelForm):
    class Meta:
        model = WatchlistItem
        fields = ["movie", "note", "priority",]
        labels = {
            "movie": "Movie",
            "note": "Your Note",
            "priority": "Priority",
        }
        widgets = {
            "movie": forms.Select(attrs={
                "class": "form-control",
            }),
            "note": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Why do you want to watch this movie?",
            }),
            "priority": forms.Select(
                choices=[
                    (1, "1 - Low"),
                    (2, "2"),
                    (3, "3 - Normal"),
                    (4, "4"),
                    (5, "5 - High"),
                ],
                attrs={
                    "class": "form-control"
                }
            ),
            
            #Insted of this down, use select
            #"priority": forms.NumberInput(attrs={
              #  "class": "form-control",
               # "min": 1,
              #  "max": 5,
           # }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.is_update = kwargs.pop("is_update", False)
        super().__init__(*args, **kwargs)

        if self.is_update:
            self.fields.pop("movie")
            return

        if self.user:
            added_movie_ids = WatchlistItem.objects.filter(
                user=self.user
            ).values_list(
                "movie_id",
                flat=True
            )

            self.fields["movie"].queryset = Movie.objects.exclude(
                id__in=added_movie_ids
            )

    def clean_note(self):
        note = self.cleaned_data["note"]
        #Down is oka but better up for 1 clean
        #note = self.cleaned_data.get("note")

        if note and len(note) > 200:
            raise forms.ValidationError(
                "Note must be under 200 characters."
            )
        
        return note