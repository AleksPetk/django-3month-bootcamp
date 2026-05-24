from django.shortcuts import render, redirect, get_list_or_404
from .models import Game, Studio
from django.db.models import Q, Avg, Max, Min, Sum, Count

# Create your views here.

def home(request):
    return render(request, "home.html")

def games(request):

    # base queryset
    games = Game.objects.all()
    studios = Studio.objects.all()
    genres = Game.objects.values_list("genre", flat=True).distinct()

    # get requests
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "newest")
    year = request.GET.get("year", "")
    multiplayer = request.GET.get("multiplayer", "")
    deleted = request.GET.get("deleted")
    min_rating = request.GET.get("min_rating", "")
    studio_id = request.GET.get("studio", "")
    genre_selected = request.GET.getlist("genre", "")

    # visibility filter
    if not deleted:
        games = games.filter(is_deleted=False)

    # search
    if query:
        games = games.filter(
            Q(title__icontains=query) |
            Q(studio__name__icontains=query) |
            Q(studio__country__icontains=query)
        )

    # filters
    if studio_id and studio_id.isdigit():
        games = games.filter(studio_id=int(studio_id))
    if multiplayer == "yes":
        games = games.filter(multiplayer=True)
    elif multiplayer == "no":
        games = games.filter(multiplayer=False)
    if min_rating and min_rating.isdigit():
        games = games.filter(rating__gte=int(min_rating))
    if year and year.isdigit() :
        games = games.filter(released_year=int(year))
    if genre_selected:
        games = games.filter(genre__in=genre_selected)

    #sort
    if sort == "oldest":
        games = games.order_by("released_year")
    elif sort == "rating":
        games = games.order_by("-rating")
    elif sort == "lowest_rating":
        games = games.order_by("rating")
    elif sort == "studio":
        games = games.order_by("studio__name")
    else:
        games = games.order_by("-released_year")

    stats = games.aggregate(
        average_rating = Avg("rating"),
        highest_rating = Max("rating"),
        lowest_rating = Min("rating")
    )
    
    # render
    return render(request, "games.html", {
        "games":games,
        "query": query,
        "count": games.count(),
        "sort": sort,
        "multiplayer": multiplayer,
        "deleted": deleted,
        "min_rating": min_rating,
        "studios": studios,
        "studio_id": studio_id,
        "year":year,
        "genres": genres,
        "genre_selected": genre_selected,
        "stats": stats
    })