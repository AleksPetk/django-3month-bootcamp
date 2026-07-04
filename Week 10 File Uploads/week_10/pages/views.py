from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import BlogPostForm, UserForm, ProfileForm
from .models import BlogPost, Profile
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    posts = BlogPost.objects.all()
    return render(request, "home.html", {"posts": posts})

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            new_user.set_password(password)
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request, new_user)
            return redirect("home")
    else:
        form = UserForm()

    context = {
        "form": form,
        "page_title": "Registration",
        "cancel_url": "home",
        "button_name": "Register"
    }
    return render(request, "page_form.html", context)
    
class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog_list.html"
    context_object_name = "posts"

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "page_form.html"
    success_url = reverse_lazy("blog_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Blog Post"
        context["cancel_url"] = "blog_list"
        context["button_name"] = "Create"
        return context
    
class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "page_form.html"
    success_url = reverse_lazy("blog_list")

    def test_func(self):
        blog = self.get_object()
        return blog.author_id == self.request.user.id or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect("home")
        return redirect("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit Blog - {self.object.title}"
        context["cancel_url"] = "blog_list"
        context["button_name"] = "Save Changes"
        context["current_image"] = self.object.cover_image
        return context
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "page_form.html"
    success_url = reverse_lazy("blog_list")

    def get_object(self):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Profile"
        context["button_name"] = "Save Profile"
        context["cancel_url"] = "blog_list"
        if self.object.avatar:
            context["current_image"] = self.object.avatar
        return context
    
class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = "delete_page.html"
    success_url = reverse_lazy("blog_list")

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Delete Blog Post: {self.object.title}"
        context["cancel_url"] = "blog_list"
        return context