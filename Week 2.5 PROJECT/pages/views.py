from django.shortcuts import render, reverse, redirect
import json
from datetime import datetime


# Create your views here.
def save_tasks(tasks, filename):
    with open(filename, "w") as f:
        json.dump(tasks, f, indent=4)

def load_tasks(filename):
    tasks = []
    try:
        with open(filename, "r", encoding="UTF-8") as f:
            tasks = json.load(f)
            return tasks
    except:
        return []

def home(request):
    website_targets = ["Make Tasks", "Count Calories", "Playground", "Django Practice", "Enjoy"]
    return render(request, "home.html", {
        "targets": website_targets
    })

def tasks(request):
    filename= "tasks.json"
    tasks = load_tasks(filename)


    if request.method == "POST":
        task = request.POST.get("task")
        tasks.append(task)
        save_tasks(tasks, filename)
        return redirect("tasks")
    
    return render(request, "tasks.html", {
        "tasks":tasks
    })

def remove_task(request, task):
    filename= "tasks.json"
    tasks = load_tasks(filename)
    if task in tasks:
        tasks.remove(task)
        save_tasks(tasks, filename)

    return redirect("tasks")
    

def calories(request):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}.json"
    todays_cal = load_tasks(filename)
    cal_n = 0
    if todays_cal:
        cal_n = todays_cal[0]

    if request.method == "POST":
        cal = request.POST.get("cal")
        cal = int(cal)
        if cal > 0:
            cal_n += cal
            todays_cal = []
            todays_cal.append(cal_n)
            save_tasks(todays_cal, filename)

            return redirect("calories")

    return render(request, "calories.html", {
        "today": today,
        "calories": cal_n
    })

house_m = {
        "Shelder": {"name":"Shelder", "open": True},
        "House": {"name": "House", "open": True},
        "Electricity": {"name": "Electricity", "open": True},
        "Water": {"name": "Water", "open": True},
}


def house(request):
    s = 0
    for key, value in house_m.items():
        if value["open"] == False:
            s += 1
    if s == 4:
        all_closed = True
    else: 
        all_closed = False

    return render(request, "house.html", {
        "house_m": house_m,
        "all_closed": all_closed
    })

def open_close(request, name):
    house_m[name]["open"] = not house_m[name]["open"]
    return redirect("house")

