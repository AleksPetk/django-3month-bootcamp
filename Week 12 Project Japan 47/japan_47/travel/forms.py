from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Place, Profile, Review

User = get_user_model()


class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, strip=False)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput, strip=False)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error("password2", "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = (
            "name",
            "description",
            "image",
            "city",
            "google_maps_url",
            "official_website",
            "travel_tips",
        )
        labels = {
            "name": "Place name",
            "description": "Description",
            "image": "Place image",
            "city": "City",
            "google_maps_url": "Google Maps URL",
            "official_website": "Official website",
            "travel_tips": "Travel tips",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the place name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe the place",
                    "rows": 5,
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the city (optional)",
                }
            ),
            "google_maps_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://maps.google.com/... (optional)",
                }
            ),
            "official_website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com (optional)",
                }
            ),
            "travel_tips": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Share useful travel tips (optional)",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in (
            "image",
            "city",
            "google_maps_url",
            "official_website",
            "travel_tips",
        ):
            self.fields[field_name].required = False


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")
        widgets = {
            "rating": forms.HiddenInput(),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Share your experience (optional)",
                    "rows": 5,
                }
            ),
        }
        labels = {
            "comment": "Your review",
        }


class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "you@example.com",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ("nickname", "email", "profile_image")
        labels = {
            "nickname": "Nickname",
            "profile_image": "Profile photo",
        }
        widgets = {
            "nickname": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "How should your name appear?",
                }
            ),
            "profile_image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.instance.user
        self.fields["email"].initial = self.user.email
        self.fields["nickname"].required = False
        self.fields["profile_image"].required = False

    def clean_nickname(self):
        return self.cleaned_data.get("nickname", "").strip()

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.email = self.cleaned_data["email"]

        if commit:
            self.user.save(update_fields=["email"])
            profile.save()

        return profile
