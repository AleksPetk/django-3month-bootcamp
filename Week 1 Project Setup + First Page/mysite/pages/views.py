

from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.

def home(request):
    return render(request, "home.html")

def about(request):
    return HttpResponse("This is about me")

def contact(request):
    return HttpResponse("Get in touch")

def hello(request, name):
    return HttpResponse(f"Hello, {name}!")

def age(request, age):
    return HttpResponse(f"You are {age} years old.")

def profile(request, name, age):
    return render(request, "profile.html", {
        "name": name.capitalize(),
        "age": age,
        "food": "Spaggethi",
        "colors": ["red", "black", "green"],
        "numbers": [1, 2, 3, 4, 5],
        "students": ["Aleks", "Mai", "Nami"],
        "is_logged_in": True,
        "check_age": age,
        "score": 99
    })

def services(request):
    return render(request, 'services.html', {
        "cars": ["Toyota", "Mitsubishi", "Nissan"],
        "hotels": ["Hilton", "Home-stay", "Matsubarashi"],
        "attractions": ["Sky-diving", "Diving", "Adult-experience"]
    })

def dashboard(request, name, score):
    if score > 100:
        return HttpResponse("Scores can't be more than 100!")
    return render(request, "dashboard.html", {
        "name": name,
        "score": score,
        "tasks": ["Study Django", "Workout", "Read Book"]
    })

def products(request):
    all_products = ["Iphone", "Laptop", "Car", "Tablet", "Radio", "TV", "Refrigirator"]
    products = random.sample(all_products, 3)
    return render(request, "products.html", {
        "products": products,
        "prices": [100, 300, 200]
    })

def score_board(request):
    return render(request, "scores.html", {
        "scores": [95, 60, 78, 88]
    })

def users(request):
    return render(request, "users.html", {"users": [
        {"name": "Aleks", "active": True},
        {"name": "Mai", "active": True},
        {"name": "Nami", "active": True},
        {"name": "Jimi", "active": False}
    ]})

def cars(request):
    cars_list = ["Toyota", "Subaru", "Mitsubishi", "Ferrari", "Nissan", "Tesla", "Daihatsu"]
    brands = ["Gucci", "Nike"]
    return render(request, "cars.html", {
        "cars_list": cars_list,
        "brands": brands
    })

def calculator_aleks(request, option, x, y):
    if x > 1000 or y > 1000:
        return HttpResponse("Too large numbers. x and y should be up to 1000.")
    if option == "multiply":
        res = x * y
    elif option == "minus":
        res = x - y
    elif option == "plus":
        res = x + y
    elif option == "divide":
        if y == 0:
            return HttpResponse("Can't divide by 0")
        res = x / y
    elif option == "power":
        res = x ** y
    else:
        return HttpResponse("Something went Wrong")
    return HttpResponse(f"{option.capitalize()}: x = {x} & y = {y} | Result: {res}")

def hub(request):
    return render(request, "hub.html", {
        "links": [
            {"name": "Home", "url_name": "home"},
            {"name": "Services", "url_name": "services"},
            {"name": "Cars", "url_name": "cars"}
        ]
    })