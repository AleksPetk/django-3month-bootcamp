from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Review
from .forms import CategoryForm, ReviewForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.

def home(request):
    return render(request, "home.html")

@login_required
def categories(request):
    categories = Category.objects.all()
    return render(request, "models/categories.html", {
        "categories": categories
    })

@login_required
def category_create(request):
    if not request.user.is_superuser:
        return redirect("categories")
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories")
    else:
        form = CategoryForm()

    pageContext = {
        "form": form,
        "page_title": "Create Category",
        "button_text": "Create",
        "cancel_url": "categories"
    }
    return render(request, "forms/page_form.html", pageContext)

@login_required
def category_edit(request, id):

    if not request.user.is_superuser:
        return redirect("categories")
    
    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories")
        
    else:
        form = CategoryForm(instance=category)

    pageContext = {
        "form": form,
        "page_title": f"Edit Category - {category.name}",
        "button_text": "Save Changes",
        "cancel_url": "categories"
    }

    return render(request, "forms/page_form.html", pageContext)

@login_required
def category_delete(request, id):
    if not request.user.is_superuser:
        return redirect("categories")
    
    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        category.delete()
        return redirect("categories")
    
    deleteContext = {
        "page_title": f"Delete Category {category.name}",
        "name": category.name,
        "id": category.id,
        "button_text": "Delete",
        "cancel_url": "categories"

    }

    return render(request, "forms/delete_form.html", deleteContext)



def reviews(request):
    reviews = Review.objects.select_related("category", "author").filter(recommended=True)
    return render(request,"models/reviews.html", {
        "reviews": reviews
    })

@login_required
def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.author = request.user
            new_review.save()
            return redirect("reviews")
    else:
        form = ReviewForm()
    
    pageContext = {
        "form": form,
        "page_title": f"Create Review",
        "button_text": "Create",
        "cancel_url": "reviews"
    }

    return render(request, "forms/page_form.html", pageContext)

@login_required
def review_edit(request, id):
    review = get_object_or_404(Review, id=id)
    if request.user.id != review.author_id:
        return redirect("reviews")
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect("reviews")
    else:
        form = ReviewForm(instance=review)

    pageContext = {
        "form": form,
        "page_title": f"Edit Review - {review.title}",
        "button_text": "Save Changes",
        "cancel_url": "reviews"
    }

    return render(request, "forms/page_form.html", pageContext)

@login_required
def review_delete(request, id):
    review = get_object_or_404(Review, id=id)

    if request.user.id != review.author_id:
        return redirect("reviews")
    
    if request.method == "POST":
        review.delete()
        return redirect("reviews")
    
    deleteContext = {
        "page_title": f"Delete Review {review.title}",
        "name": review.title,
        "id": review.id,
        "button_text": "Delete",
        "cancel_url": "reviews"

    }
    
    return render(request, "forms/delete_form.html", deleteContext)

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("home")
    else:
        form = UserForm()

    pageContext = {
        "form": form,
        "page_title": f"Register",
        "button_text": "Register",
        "cancel_url": "home"
    }
    return render(request, "forms/page_form.html", pageContext)