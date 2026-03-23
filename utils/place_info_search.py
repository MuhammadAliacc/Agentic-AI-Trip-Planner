import os
import json
from langchain_tavily import TavilySearch
# from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper 
import requests

# class GooglePlaceSearchTool:
#     def __init__(self, api_key: str):
#         self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=api_key)
#         self.places_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)
    
#     def google_search_attractions(self, place: str) -> dict:
#         """
#         Searches for attractions in the specified place using GooglePlaces API.
#         """
#         return self.places_tool.run(f"top attractive places in and around {place}")
    
#     def google_search_restaurants(self, place: str) -> dict:
#         """
#         Searches for available restaurants in the specified place using GooglePlaces API.
#         """
#         return self.places_tool.run(f"what are the top 10 restaurants and eateries in and around {place}?")
    
#     def google_search_activity(self, place: str) -> dict:
#         """
#         Searches for popular activities in the specified place using GooglePlaces API.
#         """
#         return self.places_tool.run(f"Activities in and around {place}")

#     def google_search_transportation(self, place: str) -> dict:
#         """
#         Searches for available modes of transportation in the specified place using GooglePlaces API.
#         """
#         return self.places_tool.run(f"What are the different modes of transportations available in {place}")


class OpenStreetMapTool:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"

    def _search(self, query: str):
        params = {
            "q": query,
            "format": "json",
            "limit": 5
        }

        headers = {
            "User-Agent": "trip-planner-agent"
        }

        response = requests.get(self.base_url, params=params, headers=headers)

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

    def search_attractions(self, place: str):
        return self._search(f"tourist attractions in {place}")

    def search_restaurants(self, place: str):
        return self._search(f"restaurants in {place}")

    def search_activity(self, place: str):
        return self._search(f"things to do in {place}")

    def search_transportation(self, place: str):
        return self._search(f"public transport in {place}")
    

class TavilyPlaceSearchTool:
    def __init__(self):
        pass

    def tavily_search_attractions(self, place: str) -> dict:
        """
        Searches for attractions in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"top attractive places in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    def tavily_search_restaurants(self, place: str) -> dict:
        """
        Searches for available restaurants in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}."})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    def tavily_search_activity(self, place: str) -> dict:
        """
        Searches for popular activities in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"activities in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_transportation(self, place: str) -> dict:
        """
        Searches for available modes of transportation in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"What are the different modes of transportations available in {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
