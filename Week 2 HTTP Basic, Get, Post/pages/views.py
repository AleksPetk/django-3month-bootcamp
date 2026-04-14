

from django.shortcuts import render, redirect

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

def hello_post(request):
    name = None
    age = None
    city = None
    food = None
    method = "GET"

    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        city = request.POST.get("city")
        food = request.POST.get("food")
        method = "POST"

        return redirect(f"/hello_result/?success=1&name={name}&age={age}&city={city}&food={food}")

    return render(request, "hello_post.html")



def hello_result(request):
    name = request.GET.get("name", "Guest")
    age = request.GET.get("age", "No Age")
    city = request.GET.get("city", "City")
    food = request.GET.get("food", "Sushi")
    success = request.GET.get("success")
    if success == "1":

        if food:
            food.capitalize()
        else:
            food = "No food added"

        if age.isdigit():
            age = int(age)
        else:
            age = "No proper age added"

        return render(request, "hello_result.html", {
            "data": {
                "Success":"You successfuly Submit",
                "Name": name.capitalize(),
                "Age": age,
                "City":city.capitalize(),
                "Food":food
            }
        })



def search(request):
    search_for = request.GET.get("search_for")
    
    return render(request, "search.html", {
        "search_for": search_for
    })

