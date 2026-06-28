from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import UserForm, GameForm
from .models import Game

# Create your views here.

def home(request):
    return render(request, "home.html")


def register(request):
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
    }
    return render(request, "page_form.html", context)

class GameListView(ListView):
    model = Game
    template_name = "games.html"
    context_object_name = "games"
    paginate_by = 3

    def get_queryset(self):
        return Game.objects.select_related("owner")
    
class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = "page_form.html"
    #success_url = reverse_lazy("games")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create New Game"
        context["cancel_url"] = "games"
        return context
    
    def get_success_url(self):
        return reverse_lazy(
            "game_details",
            kwargs={
                "pk":self.object.pk
            }
        )
    
class GameDetailView(DetailView):
    model = Game
    template_name = "game_details.html"
    context_object_name = "game"

class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = "page_form.html"
    success_url = reverse_lazy("games")

    def test_func(self):
        game = self.get_object()
        return game.owner_id==self.request.user.id
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect("login")
        
        return redirect("games")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit Game - {self.object.title}"
        context["cancel_url"] = "games"
        return context

class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Game
    success_url = reverse_lazy("games")
    template_name = "delete_page.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Game.objects.all()
        return Game.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Delete Game - {self.object.title}"
        context["cancel_url"] = "games"
        return context
