from django.shortcuts import render, get_object_or_404
from .models import Car, Game, Movie

# Create your views here.

def home(request):
    return render(request, "home.html")

def movie(request):
    movies = Movie.objects.all()
    return render(request, "movies.html", {
        "movies": movies,
        "count": len(movies)
    })

def movie_details(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, "movie_details.html", {
        "movie": movie
    })

def car(request):
    cars = Car.objects.all()
    return render(request, "cars.html", {
        "cars": cars,
        "count": len(cars)
    })

def car_details(request, id):
    car = get_object_or_404(Car, id=id)
    return render(request, "car_details.html", {
        "car": car
    })

def games(request):
    games = Game.objects.filter(rating__gte = 2)
    return render(request, "games.html", {
        "games": games,
        "count": len(games)
    })

def game_details(request, id):
    game = get_object_or_404(Game, id=id)
    
    if game.rating >= 3:
        rate = "Exellent"
    elif game.rating >= 2:
        rate =  "Good"
    else:
        rate = "Bad"
    return render(request, "game_details.html", {
        "game": game,
        "rate": rate
    })