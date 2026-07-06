from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .models import DevBlog

from .forms import DevBlogForm, UserForm

# Create your views here.


def home(request):
    return render(request, "home.html")


"""def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            new_user.set_password(password)
            new_user.save()
            login(request, new_user)
            return redirect("home")
    else:
        form = UserForm()
    context = {
        "form": form,
        "page_title": "Register",
        "cancel_url": "home",
        "button_name": "Register"
    }
    return render(request, "page_form.html", context)"""

class RegisterCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = "page_form.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        new_user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        new_user.set_password(password)
        new_user.save()
        login(self.request, new_user)
        return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Register"
        context["button_name"] = "Register"
        context["cancel_url"] = "home"
        return context

class DevBlogListView(ListView):
    model = DevBlog
    template_name = "devblog_list.html"
    context_object_name = "posts"

    paginate_by = 3

    def get_queryset(self):
        return DevBlog.objects.select_related("author", "category").all()

class DevBlogDetailView(DetailView):
    model = DevBlog
    template_name = "devblog_detail.html"
    context_object_name = "post"
    def get_object(self):
        post = get_object_or_404(
            DevBlog,
            pk=self.kwargs["pk"]
        )
        return post
    
class DevBlogCreateView(LoginRequiredMixin, CreateView):
    model = DevBlog
    form_class = DevBlogForm
    success_url = reverse_lazy("devblogs")
    template_name = "page_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create DevBlog"
        context["cancel_url"] = "devblogs"
        context["button_name"] = "Create"
        return context
    
class DevBlogUpdateView(LoginRequiredMixin, UpdateView):
    model = DevBlog
    form_class = DevBlogForm
    template_name = "page_form.html"
    success_url = reverse_lazy("devblogs")

    def get_queryset(self):
        return DevBlog.objects.filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Update: {self.object.title}"
        context["button_name"] = "Update"
        context["cancel_url"] = "devblogs"
        return context
    
class DevBlogDeleteView(LoginRequiredMixin, DeleteView):
    model = DevBlog
    template_name = "page_delete.html"
    success_url = reverse_lazy("devblogs")

    def get_queryset(self):
        return DevBlog.objects.filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Delete: {self.object.title}"
        context["cancel_url"] = "devblogs"
        return context
