from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, NoteForm, TaskForm, UserForm, PostForm, EventForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Note, Task, Post, Event, Category
from django.utils import timezone

# Create your views here.

def home(request):
    return render(request, "home.html")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = ContactForm()
    return render(request, 'contact.html', {
        "form": form
    })

@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            Note.objects.create(
                title = form.cleaned_data["title"],
                content = form.cleaned_data["content"],
                author = request.user
            )
            return redirect('notes')
    else:
        form = NoteForm()
    return render(request, "note_form.html", {
        "form": form
    })

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("posts")
    else:
        form = PostForm()
    return render(request, "post_form.html", {
        "form": form
    })

def posts(request):
    posts = Post.objects.filter(published=True)
    return render(request, "posts.html", {
        "posts": posts
    })

def notes(request):
    notes = Note.objects.select_related("author").all()
    return render(request, "notes.html", {
        "notes": notes
    })

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserForm()
    return render(request, "register.html", {
        "form": form
    })

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect("tasks")
    else:
        form = TaskForm()
    return render(request, "form_page.html", {
        "form": form,
        "page_title": "Create Task",
        "button_text": "Create",
        "cancel_url": "tasks"
    })

def tasks(request):
    tasks = Task.objects.select_related("owner").filter(completed=False)
    return render(request, "tasks.html", {
        "tasks": tasks
    })

@login_required
def task_edit(request, id):
    task = get_object_or_404(Task, id=id)

    if task.owner_id != request.user.id:
        return redirect("tasks")
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("tasks")
        
    else:
        form = TaskForm(instance=task)

    return render(request, "form_page.html", {
        "form": form,
        "page_title": "Edit Task",
        "button_text": "Save Changes",
        "cancel_url": "tasks"
    })

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id)

    if task.owner_id != request.user.id:
        return redirect("tasks")
    if request.method == "POST":
        task.delete()
        return redirect("tasks")
    
    return render(request, "delete_form.html", {
        "object": task,
        "page_title_name": f"{task.title}",
        "cancel_url": "tasks"
    })

def events(request):
    today = timezone.now().date()
    events = Event.objects.filter(start_date__lte=today, end_date__gte=today, is_public=True)
    return render(request, "events.html", {
        "events": events
    })

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("events")
    else:
        form = EventForm()
    return render(request, "form_page.html", {
        "form": form,
        "page_title": "Create Event",
        "button_text": "Create",
        "cancel_url": "events"
    })

@login_required
def event_edit(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("events")
        
    else:
        form = EventForm(instance=event)

    return render(request, "form_page.html", {
        "form": form,
        "page_title": "Edit Event",
        "button_text": "Save Changes",
        "cancel_url": "events"
    })

@login_required
def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        event.delete()
        return redirect("events")
    return render(request, "delete_form.html", {
        "object": event,
        "page_title_name": f"{event.title}",
        "cancel_url": "events"
    })


@login_required
def categories(request):
    categories = Category.objects.all()

    return render(request, "categories.html", {
        "categories": categories
    })

@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories")
    else:
        form = CategoryForm()
    return render(request, "form_page.html", {
        "form": form,
        "page_title": "Create Category",
        "button_text": "Create",
        "cancel_url": "categories"
    })

@login_required
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories")
    else:
        form = CategoryForm(instance=category)
    
    return render(request, "form_page.html", {
        "form": form,
        "page_title": f"Edit Category - {category.name}",
        "button_text": "Save Changes",
        "cancel_url": "categories"
    })

@login_required
def category_delete(request, id):
    if not request.user.is_superuser:
        return redirect("categories")
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        category.delete()
        return redirect("categories")
    
    return render(request, "delete_form.html", {
        "object": category,
        "page_title_name": f"{category.name}",
        "cancel_url": "categories"
    })