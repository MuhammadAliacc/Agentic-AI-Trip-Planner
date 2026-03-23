import requests

def search_places(query: str):
    url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        "q": query,
        "format": "json",
        "limit": 5
    }

    headers = {
        "User-Agent": "trip-planner-app"  # IMPORTANT (required by OSM)
    }

    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}

    data = response.json()

    results = []
    for place in data:
        results.append({
            "name": place.get("display_name"),
            "lat": place.get("lat"),
            "lon": place.get("lon")
        })

    return results