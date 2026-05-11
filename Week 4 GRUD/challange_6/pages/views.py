from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from .models import Anime, Movie, Author


# Create your views here.
def make_unique_slug(title, Model):
    base_slug = slugify(title) or "item"
    slug = base_slug
    num = 1
    while Model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{num}"
        num += 1
    return slug


def helper_all(Model):
    models = Model.objects.filter(is_deleted=False)
    return models

def home(request):
    movies = helper_all(Movie)
    animes = helper_all(Anime)
    authors = Author.objects.all()
    return render(request, "home/home.html", {
        "movies": movies[:3],
        "animes": animes[:3],
        "authors": authors[:3]
    })

def animes(request):
    animes = helper_all(Anime)

    return render(request, "animes/animes.html", {
        "animes": animes,
        "count": len(animes)
    })

def movies(request):
    movies = helper_all(Movie)

    return render(request, "movies/movies.html", {
        "movies": movies,
        "count": len(movies)
    })

def authors(request):
    authors = Author.objects.all()

    return render(request, "authors/authors.html", {
        "authors": authors,
        "count": len(authors)
    })


def anime_details(request, slug):
    anime = get_object_or_404(Anime, slug=slug, is_deleted=False)

    return render(request, "animes/anime_details.html", {
        "anime": anime
    })

def movie_details(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_deleted=False)

    return render(request, "movies/movie_details.html", {
        "movie": movie
    })

def author_details(request, slug):
    author = get_object_or_404(Author, slug=slug)

    return render(request, "authors/author_details.html", {
        "author": author
    })

def anime_create(request):
    error = ""
    authors = Author.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        released_year = request.POST.get("released_year")
        rating = request.POST.get("rating")
        author_id = request.POST.get("author_id")
        author = get_object_or_404(Author, id = author_id)
        slug = make_unique_slug(title, Anime)
        if title and released_year and rating:
            new_anime = Anime.objects.create(
                title = title,
                released_year = released_year,
                rating = rating,
                author = author,
                slug = slug
            )
            return redirect("anime_details", new_anime.slug)
    return render(request, "animes/anime_form.html", {
        "error": error,
        "authors": authors
    })

def anime_edit(request, slug):
    anime = get_object_or_404(Anime, slug=slug, is_deleted = False)
    error = ""
    authors = Author.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        released_year = request.POST.get("released_year")
        rating = request.POST.get("rating")
        slug = make_unique_slug(title, Anime)
        if title and released_year and rating:
            anime.title = title
            anime.released_year = released_year
            anime.rating = rating
            anime.slug = slug
            anime.save()
            return redirect("anime_details", anime.slug)
    return render(request, "animes/anime_form.html", {
        "error": error,
        "anime": anime,
        "authors":authors
    })

def anime_delete(request, slug):
    anime = get_object_or_404(Anime, slug=slug, is_deleted=False)

    if request.method == "POST":
        anime.is_deleted = True
        return redirect("animes")
    
    return render(request, "animes/anime_delete.html", {
        "anime":anime
    })

def movie_create(request):
    error = ""
    authors = Author.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        released_year = request.POST.get("released_year")
        rating = request.POST.get("rating")
        author_id = request.POST.get("author_id")
        author = get_object_or_404(Author, id = author_id)
        slug = make_unique_slug(title, Movie)
        if title and released_year and rating:
            new_movie = Movie.objects.create(
                title = title,
                released_year = released_year,
                rating = rating,
                author = author,
                slug = slug
            )
            return redirect("movie_details", new_movie.slug)
    return render(request, "movies/movie_form.html", {
        "error": error,
        "authors": authors
    })

def movie_edit(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_deleted = False)
    error = ""
    authors = Author.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        released_year = request.POST.get("released_year")
        rating = request.POST.get("rating")
        slug = make_unique_slug(title, Movie)
        if title and released_year and rating:
            movie.title = title
            movie.released_year = released_year
            movie.slug = slug
            movie.rating = rating
            movie.save()
            return redirect("movie_details", movie.slug)
    return render(request, "movies/movie_form.html", {
        "error": error,
        "movie": movie,
        "authors":authors
    })

def movie_delete(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_deleted=False)

    if request.method == "POST":
        movie.is_deleted = True
        return redirect("movies")
    
    return render(request, "movies/movie_delete.html", {
        "movie":movie
    })

def author_create(request):
    error = ""
    if request.method == "POST":
        name = request.POST.get("name")
        year_born = request.POST.get("year_born")
        slug = make_unique_slug(name, Author)
        if name and year_born:
            new_author = Author.objects.create(
                name = name,
                year_born = year_born,
                slug = slug
            )
            return redirect("author_details", new_author.slug)
    return render(request, "authors/author_form.html", {
        "error": error
    })

def author_delete(request, slug):
    author = get_object_or_404(Author, slug=slug)

    if request.method == "POST":
        author.delete()
        return redirect("authors")
    
    return render(request, "authors/author_delete.html", {
        "author":author
    })