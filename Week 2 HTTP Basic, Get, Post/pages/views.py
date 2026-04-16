

import json

from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.

filename = "products.json"

def loads_j():
    products = []
    try:
        with open(filename, "r", encoding="UTF-8") as f:
            products = json.load(f)
            return products
    except:
        pass

def save_j(products):
    with open(filename, "w") as f:
        json.dump(products, f, indent=4)

def home(request):
    name = "Aleks"
    hobby = "Motorbikes"
    age = 28
    website_mean = "This website is only for educational purpose"
    my_list = [name, hobby, age, website_mean]
    return render(request, "home.html", {
        "my_list": my_list
    })

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

    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        city = request.POST.get("city")
        food = request.POST.get("food")
        url = reverse("hello_result")

        return redirect(f"{url}?success=1&name={name}&age={age}&city={city}&food={food}")

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

def info_post(request):

    if request.method == "POST":
        f_name = request.POST.get("f_name")
        l_name = request.POST.get("l_name")
        email = request.POST.get("email")
        date = request.POST.get("date")
        mot = request.POST.get("mot")
        if not mot:
            mot = "No Motivation"
        url = reverse("info_redirect")

        return redirect(f"{url}?f_name={f_name}&l_name={l_name}&email={email}&date={date}&mot={mot}")
        

    return render(request, "info_post.html")

def info_redirect(request):
    f_name = request.GET.get("f_name")
    l_name = request.GET.get("l_name")
    email = request.GET.get("email")
    date = request.GET.get("date")
    mot = request.GET.get("mot")
    return render(request, "info_redirect.html", {
        "f_name": f_name,
        "l_name": l_name,
        "email": email,
        "date": date,
        "mot": mot
    })


def task(request):
    if request.method == "POST":
        name = request.POST.get("name")
        explain = request.POST.get("explain")

        url = reverse("task_view")

        return redirect(f"{url}?name={name}&explain={explain}")
    return render(request, "task.html")

def task_view(request):
    name = request.GET.get("name", "empty")
    explain = request.GET.get("explain", "empty")
    if not explain:
        explain = "No explanation"
    return render(request, "task_view.html", {
        "name": name,
        "explain": explain
    })

def delete_task(request, task_name):
    url = reverse("delete_result")
    return redirect(f"{url}?task={task_name}")

def delete_result(request):
    task = request.GET.get("task")
    return render(request, "delete_result.html", {
        "task": task
    })
def task_menu(request):
    tasks = ["Eat", "Sleep", "Watch", "Study Django", "Workout", "Reading"]
    return render(request, "task_menu.html", {
        "tasks": tasks
    })

def product(request):
    products = loads_j()

    if request.method == "POST":
        name = request.POST.get("name")
        check = 0
        if not name:
            return redirect('products')
        for product in products:
            if product["text"]:
                if product["text"] == name:
                    
                    return redirect("products")
                
        name = {"text": name, "available": True}
        products.append(name)
        save_j(products=products)
        return redirect("products")
    
    status = request.GET.get("status")

    return render(request, "products.html", {
        "products": products,
        "status": status
    })

def del_product(request, name):
    i = 0
    products = loads_j()
    for product in products:
        if product["text"] == name:
            del products[i]
            save_j(products=products)
            print("deleted")
            
            return redirect("products")
            
        i += 1
    return redirect("products")

def sell_p(request, name, num):
    products = loads_j()
    for product in products:
        if product["text"] == name:
            if num == 1:
                product["available"] = False
            elif num == 2:
                product["available"] = True

            save_j(products=products)
            return redirect("products")

