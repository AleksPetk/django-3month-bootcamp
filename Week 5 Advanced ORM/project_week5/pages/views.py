from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Max, Min, Q
from .models import Anime, Studio

# Create your views here.

def home(request):
    return render(request, "home.html")

def animes(request):
    # base queryste
    animes = Anime.objects.select_related("studio").all()

    # get requests
    query = request.GET.get("q", "")
    ongoing = request.GET.get("ongoing", "")
    is_deleted = request.GET.get("is_deleted", "")
    ranking = request.GET.get("ranking", "")

    # dropdown data
    rankings = animes.values_list("rating", flat=True).distinct().order_by("-rating")

    # Search title contains or studio contains
    if query:
        animes = animes.filter(
            Q(title__icontains = query) |
            Q(studio__name__icontains = query)
        )

    #Visability
    if is_deleted:
        if is_deleted == "all":
            pass
        elif is_deleted == "yes":
            animes = animes.filter(is_deleted=True)
    else:
        animes = animes.filter(is_deleted=False)

    # Filters ongoing,     
    if ongoing:
        if ongoing == "yes":
            animes = animes.filter(ongoing=True)
        elif ongoing == "no":
            animes = animes.filter(ongoing=False)

    if ranking and ranking.isdigit():
        animes = animes.filter(rating=int(ranking))

        

    return render(request, "animes.html", {
        "animes": animes,
        "count": len(animes),
        "ongoing": ongoing,
        "query": query,
        "is_deleted": is_deleted,
        "rankings": rankings,
        "ranking": ranking
    })

def anime_delete(request, id):
    anime = get_object_or_404(Anime, id=id)
    if anime:
        if request.method == "POST":
            anime.is_deleted = True
            anime.save()
            return redirect("animes")
