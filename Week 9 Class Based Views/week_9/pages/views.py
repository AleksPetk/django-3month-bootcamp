from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Anime, Movie, WatchlistItem
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import MovieForm, UserForm, WatchlistItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


# Create your views here.

def home(request):
    return render(request, "home.html")

def reviews(request):
    reviews = Review.objects.filter(recommended=True)
    return render(request, "reviews.html", {
        "reviews": reviews
    })

class ReviewListView(ListView):
    model = Review
    template_name = "reviews.html"
    context_object_name = "reviews"
    paginate_by = 1
    def get_queryset(self):
        return Review.objects.filter(recommended=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Recommended Reviews"
        context["count_rev"] = self.get_queryset().count()
        return context
    
class ReviewAllListView(ListView):
    model = Review
    template_name = "reviews.html"
    context_object_name = "reviews"
    paginate_by = 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context["page_title"] = "All Reviews"
        context["count_rev"] = self.get_queryset().count()
        return context
    
class AnimeList(ListView):
    
    model = Anime
    template_name = "animes.html"
    context_object_name = "animes"

    paginate_by = 3
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Animes"
        context["count_rev"] = self.get_queryset().count()
        return context
    
class ReviewDetailView(DetailView):
    model = Review
    template_name = "review_detail.html"
    context_object_name = "review"

    def get_object(self):

        review = get_object_or_404(
            Review,
            pk=self.kwargs["pk"]
        )
        if review.recommended:
            return review
        if self.request.user.is_superuser:
            return review
        raise Http404
        
#Movies

#FBV
"""def movies(request):
    movies = Movie.objects.filter(watched=True)
    return render(request, "movies.html", {
        "movies": movies
    })"""

#CBV
class MovieListView(ListView):
    model = Movie
    template_name = "movies.html"
    context_object_name = "movies"
    paginate_by = 3


#FBV
"""@login_required
def movie_create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_user = request.user
            movie.save()
            return redirect("movies")
    else:
        form = MovieForm()

    context = {
        "form": form,
        "page_title": "Add New Movie",
        "cancel_url": "movies",
    }
    return render(request, "page_form.html", context)"""
#CBV
class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = "page_form.html"
    #success_url = reverse_lazy("movies")
    
    def form_valid(self, form):
        form.instance.added_user = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add New Movie"
        context["cancel_url"] = "movies"
        return context
    
    def get_success_url(self):
        return reverse_lazy(
            "movie_details",
            kwargs={
                "pk": self.object.pk
            }
        )


#FBV
"""@login_required
def movie_edit(request, id):
    movie = get_object_or_404(Movie, id=id)
    if movie.added_user_id != request.user.id:
        return redirect("movies")
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect("movies")
    else:
        form = MovieForm(instance=movie)

    context = {
        "form": form,
        "page_title": f"Edit Movie: {movie.title}",
        "cancel_url": "movies",
    }
    return render(request, "page_form.html", context)"""

#CBV
class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = "page_form.html"
    success_url = reverse_lazy("movies")
    #login_url = "movies"

    def test_func(self):
        movie = self.get_object()
        return movie.added_user_id == self.request.user.id or self.request.user.is_superuser
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect("login")
        return redirect("movies")

    """def dispatch(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, pk=kwargs["pk"])

        if movie.added_user.id != request.user.id:
            return redirect("movies")
        
        return super().dispatch(request, *args, **kwargs)"""

    """def get_queryset(self):
        return Movie.objects.filter(added_user=self.request.user)"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit Movie: {self.object.title}"
        context["cancel_url"] = "movies"
        return context


#FBV
"""@login_required
def movie_delete(request, id):
    movie = get_object_or_404(Movie, id=id)
    if movie.added_user_id != request.user.id and not request.user.is_superuser:
        return redirect("movies")
    if request.method == "POST":
        movie.delete()
        return redirect("movies")
    
    context = {
        "object": movie,
        "page_title": f"Delete Movie: {movie.title}",
        "cancel_url": "movies",
    }
    return render(request, "page_delete.html", context)"""

#CBV
class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = "page_delete.html"
    success_url = reverse_lazy("movies")

    """def dispatch(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, pk=kwargs["pk"])
        if movie.added_user.id != self.request.user.id:
            return redirect("movies")
        return super().dispatch(request, *args, **kwargs)"""

    #When use dispatch in situation like this, queryset became unnessassery
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Movie.objects.all()
        return Movie.objects.filter(added_user = self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Delete Movie: {self.object.title}"
        context["cancel_url"] = "movies"
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie_details.html"
    context_object_name = "movie"

    


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            password_confirm = form.cleaned_data.get("password_confirm")
            if password != password_confirm:
                form.add_error("password_confirm", "Passwords do not match.")
            else:
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



class WatchlistListView(LoginRequiredMixin, ListView):
    model = WatchlistItem
    template_name = "watchlist.html"
    context_object_name = "items"

    def get_queryset(self):
        return (
            WatchlistItem.objects
            .select_related("movie", "user")
            .filter(user=self.request.user)
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "My Watchlist"
        return context
    
class WatchlistCreateView(LoginRequiredMixin, CreateView):
    model = WatchlistItem
    form_class = WatchlistItemForm
    template_name = "page_form.html"
    success_url = reverse_lazy("watchlist")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Movie to Watchlist"
        context["cancel_url"] = "watchlist"
        return context

class WatchlistUpdateView(LoginRequiredMixin, UpdateView):
    model = WatchlistItem
    form_class = WatchlistItemForm
    template_name = "page_form.html"
    success_url = reverse_lazy("watchlist")

    def get_queryset(self):
        return WatchlistItem.objects.filter(
            user=self.request.user
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["is_update"] = True
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit Watchlist: {self.object.movie.title}"
        context["cancel_url"] = "watchlist"
        return context
        
class WatchlistDeleteView(LoginRequiredMixin, DeleteView):
    model = WatchlistItem
    template_name = "page_delete.html"
    success_url = reverse_lazy("watchlist")

    def get_queryset(self):
        return WatchlistItem.objects.filter(
            user=self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Remove from Watchlist: {self.object.movie.title}"
        context["cancel_url"] = "watchlist"
        return context