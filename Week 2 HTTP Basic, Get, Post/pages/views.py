

from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "home.html")

def hello_get(request):
    name = request.GET.get("name", "No Entered")
    age = request.GET.get("age", "No Entered")
    city = request.GET.get("city", "No Entered")
    food = request.GET.get("food")
    if age.isdigit():
        age = int(age)

    return render(request, "hello_get.html", {
        "name": name.capitalize(),
        "age":age,
        "city": city.capitalize(),
        "food": food
    })

def search(request):
    search_for = request.GET.get("search_for")
    
    return render(request, "search.html", {
        "search_for": search_for
    })

