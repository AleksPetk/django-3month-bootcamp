import random

from django.shortcuts import render



# Create your views here.

def home(request):
    return render(request, "home.html", {
        "title":"Hello to my website",
        "desc": "This website is only about practice Django with Gpt.",
        "things": ["Places to visit in Japan", "Contact Information", "About Joining Us"]
    })

def about(request):
    return render(request, "about.html", {
        "is_open": True,
        "open": "This Website is Open",
        "close": "This Website is Closed"
    })

def contact(request):
    return render(request, "contact.html", {
        "info": {
            "email": "jimi@gmail.com",
            "phone": "080829321",
            "city": "Tokyo"
            }
    })

places_data = {"Tokyo":{"name":"Tokyo", "country": "Japan", "rating": 5, "description": "Modern city with tradition."}, 
               "Paris": {"name":"Paris", "country": "France", "rating": 3, "description": "Old city with a lot of rubbish."}, 
               "London": {"name":"London", "country": "UK", "rating": 2, "description": "Big old city with many criminals."}, 
               "New-York": {"name":"New-York", "country": "USA", "rating": 1, "description": "Big city with more homeless people than people with home."}, 
               "Gabrovo": {"name":"Gabrovo", "country": "Bulgaria", "rating": 4, "description": "Longest city in Bulgaria, with best nature around it."}, 
               "Berlin":{"name":"Berlin", "country": "German", "rating": 2, "description": "Still dirty from Hittler time."}, 
               "Osaka": {"name":"Osaka", "country": "Japan", "rating": 4, "description": "Amazing big Japanese city, but still not Tokyo."}, 
               "Bangkok": {"name":"Bangkok", "country": "Thailand", "rating": 3, "description": "Great, funny city, but too many ladyboys."}, 
               "Fujinomiya": {"name":"Fujinomiya", "country": "Japan", "rating": 5, "description": "Great place where Aleks lives."}, 
               "Lovech": {"name":"Lovech", "country": "Bulgaria", "rating": 2, "description": "Shame city in Bulgaria."}
               }

def places(request):
    return render(request, "places.html", {
        "places": places_data,
        "rating": "rating",
        "compare": "compare",
        "random_place": "random_place"
    })

def country(request, name):
    if name in places_data.keys():
        return render(request, "place_detail.html", {
            'name': name,
            "data": places_data[name]
            })
    elif name == "rating":
        return render(request, "rating_main.html", {
        "rating": [1, 2, 3, 4, 5]
        })
    elif name == "compare":
        return render(request, "compare.html", {
            'data': dict(sorted(places_data.items(), key=lambda item: item[1]['rating'], reverse=True))
        })
    elif name == "random_place":
        list_p = []
        for value in places_data.values():
            list_p.append(value)

        return render(request, "random.html", {
            "random_p": random.choice(list_p)
        })

    
def rating(request, rating):
    ranked = []
    for value in places_data.values():
        if value['rating'] == rating:
            ranked.append(value)

    if ranked:
        return render(request, 'rating.html', {
            "ranked": ranked,
            "rating": rating
        })
    
