places_data = {"Tokyo":{"name":"Tokyo", "country": "Japan", "rating": 5, "description": "Modern city with tradition."}, 
               "Paris": {"name":"Paris", "country": "France", "rating": 3, "description": "Old city with a lot of rubbish."}, 
               "London": {"name":"London", "country": "UK", "rating": 2, "description": "Big old city with many criminals."}, 
               "New-York": {"name":"New-York", "country": "USA", "rating": 1, "description": "Big city with more homeless people than people with home."}, 
               "Gabrovo": {"name":"Gabrovo", "country": "Bulgaria", "rating": 4, "description": "Longest city in Bulgaria, with best nature around it."}}

name = "Tokyo"

data_list = []

if name in places_data.keys():
    data_list.append(places_data[name])

print(data_list[0]["name"])