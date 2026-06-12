
from django import forms
from .models import Task, Post, Event, Category
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class NoteForm(forms.Form):
    title = forms.CharField(
        min_length=3,
        max_length=50,
        label="Note Title",
        help_text="3-50 characters",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Enter note title"
        })
    )
    content = forms.CharField(
        min_length=10,
        label="Note Content",
        help_text="At least 10 characters",
        widget=forms.Textarea(attrs={
            "class": "form-textarea",
            "placeholder": "Write you note...",
            "rows": 5
        })
    )
    is_public = forms.BooleanField(
        required=False,
        label="Make public"
    )
    def clean_title(self):
        title = self.cleaned_data["title"].strip().title()
        if len(title) < 5:
            raise forms.ValidationError(
                "Actually it should be 5 or more, catch you."
            )

        if "test" in title.lower():
            raise forms.ValidationError(
                "Title cannot contains the word test."
            )
        bad_words = ["shit", "stupid", "idiot", "fuck", "suck", "pussy", "dick"]
        for word in bad_words:
            if word in title.lower():
                raise forms.ValidationError(
                    "Do not use bad words!"
                )
        return title
    
    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if title and content:
            if title.lower() == content.lower():
                raise forms.ValidationError(
                    "Title and content cannot be identical."
                )
        return cleaned_data
    
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        
        
        fields = [
            "title",
            "description",
            "priority",
            "completed",
        ]

        labels = {
            "title": "Task Title",
            "description": "Task Description",
            "priority": "Priority Level",
            "completed": "Completed ?",
        }

        help_texts = {
            "priority": "Use 1 for low priority and higher numbers for more important tasks.",
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter task title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Describe the task...",
                "rows": 5
            }),
            "priority": forms.NumberInput(attrs={
                "class": "form-input",
                "min": 1,
                "max": 5
            }),
            "completed": forms.CheckboxInput(attrs={
                "class": "form-checkbox"
            }),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if "test" in title.lower():
            raise forms.ValidationError(
                "Task title cannot contains 'test'."
            )
        return title.title()
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")

        if title and description:
            if title.lower() == description.lower():
                raise forms.ValidationError(
                     "Title and description cannot be fucking same!"
                )

        return cleaned_data
    

class UserForm(forms.ModelForm):

    password_confirm = forms.CharField(
        min_length=8,
        label= "Confirm Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm Password",
            "class": "form-input",
        })
    )

    class Meta:
        model = User

        fields = [
            "username",
            "password",
        ]

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
                "placeholder": "Enter Password",
                "class": "form-input"
            }),
        }
        help_texts = {
            "password": "Password must be atleast 8 characters",
        }

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 8:
            raise forms.ValidationError(
                "Password less than 8 c."
            )
        return password

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if len(username) < 3:
            raise forms.ValidationError(
                "Username too short! Should be over 3 characters"
            )
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username is already taken."
            )
        if "admin" in username.lower():
            raise forms.ValidationError(
                "Username cannot contain 'admin'."
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
        if password and username:
            if username.lower() in password.lower() or password.lower() in username.lower():
                raise forms.ValidationError(
                    "Password cannot be too similar to username."
                )

        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            "title",
            "content",
            "published",
        ]

        labels = {
            "title": "Title",
            "content": "Content",
            "published": "Published",
        }

        help_texts = {
            "content": "Should be at least 50 characters long."
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter Title"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-area",
                "placeholder": "Enter you content here ...",
                "rows": 5
            }),
            "published": forms.CheckboxInput(attrs={
                "class": "form-checkbox",

            }),
        }
    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        title = f"{title} Fuck you"

        return title
    
    def clean_content(self):
        content = self.cleaned_data["content"].strip()

        if len(content) < 50:
            content = f"""I told you many times, is even written there, over 50 characters! Are you dumb?!
                    Now fuck off with this post, and what is this '{content}' no fucking nothing!
                    Now enjoy this long content!"""
            count = len(content)
            content = f"{content} | All together {count} characters"
        
        return content


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            "title",
            "description",
            "start_date",
            "end_date",
            "max_people",
            "is_public"
        ]

        labels = {
            "title": "Event Title",
            "description": "Event Description",
            "start_date": "Start Date",
            "end_date": "End Date",
            "max_people": "Max Capacity",
            "is_public": "Is Public ?"
        }

        help_texts = {
            "description": "Between 50 - 300 characters."
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "text-input",
                "placeholder": "Enter Title"
            }),
            "description": forms.Textarea(attrs={
                "class": "text-input",
                "placeholder": "Explain about the event...",
                "rows": 5          
            }),
            "start_date": forms.DateInput(attrs={
                "type": "date",
                "class": "text-input"
            }),
            "end_date": forms.DateInput(attrs={
                "type": "date",
                "class": "text-input"
            }),
            "max_people": forms.NumberInput(attrs={
                "class": "text-input",
                "min": 1,
                "max": 100
            }),
            "is_public": forms.CheckboxInput(attrs={
                "class": "text-input"
            })
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].help_text = (
            "Choose a clear event title."
        )

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        errors = []
        bad_words = ["fuck", "suck", "dick", "kill", "idiot"]

        if "admin" in title.lower():
            errors.append("Title cannot contains 'admin'.")

        for word in bad_words:
            if word in title.lower():
                errors.append("Title cannot contains bad words.")
                break

        if errors:
            raise forms.ValidationError(
                errors
            )

        return title
    
    def clean_max_people(self):
        max_people = self.cleaned_data["max_people"]

        if max_people < 1 or max_people > 100:
            raise forms.ValidationError(
                "Capacity should be between 1-100."
            )
        return max_people
    
    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        description = cleaned_data.get("description")
        is_public = cleaned_data.get("is_public")

        if start_date and end_date:
            if end_date < start_date:
                self.add_error(
                    "end_date",
                    "End date cannot be before Start date."
                )
        if is_public and description:
            if len(description) < 50 or len(description) > 300:
                self.add_error(
                    "description",
                    "Public Event description must between 50-300 characters"
                )
        if description:
            if "suck" in description.lower():
                raise forms.ValidationError(
                    "Cant suck!"
                )
        return cleaned_data
    
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
            "description"
        ]

        labels = {
            "name": "Name",
            "description": "Description"
        }

        help_texts = {
            "name": "From 5-50 characters.",
            "description": "At least 20 characters."
        }

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "text-input",
                "placeholder": "Enter name"
            }),
            "description": forms.Textarea(attrs={
                "class": "text-input",
                "placeholder": "Describe...",
                "rows": 5
            })
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        bad_words = ["suck", "dick", "lick", "pussy", "porno", "bastard", "kurva"]

        for word in bad_words:
            if word in name.lower():
                raise forms.ValidationError(
                    f"'{word}' cannot be used in Name!"
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

        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if description and name:
            if name.lower() == description.lower():
                raise forms.ValidationError(
                    "Name and Description cannot be same."
                )
            if len(name) > len(description):
                raise forms.ValidationError(
                    "Name cannot be longer than description."
                )
            
        return cleaned_data