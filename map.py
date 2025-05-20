import requests
from langchain_groq import ChatGroq
import os

def recommend(l, lo, inp):
    headers = {
        "User-Agent": "MyLocationApp/1.0 (your_email@example.com)"
    }

    # Convert latitude and longitude from string to float
    latitude = float(l)
    longitude = float(lo)

    viewbox = f"{longitude - 0.10},{latitude + 0.10},{longitude + 0.10},{latitude - 0.10}"

    kk = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(groq_api_key=kk, model_name="gemma2-9b-it", temperature=0.5)

    b = llm.invoke(f"{inp}:<-- if the first given text is related to drugstore or pharmacy or things like that give True as output else False ")

    if bool(b.content) and "True" in b.content:
        a = ["Drugstore", "Chemist", "Apothecary", "Dispensary", "Medicinal store", "Health food store", "Chemist shop", "Medication store", "pharmacy"]
        s = ''
        for i in a:
            query = i
            search_url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=5&bounded=1&viewbox={viewbox}"
            search_response = requests.get(search_url, headers=headers)
            results = search_response.json()

            for place in results:
                s += f"- {place['display_name']}\n"

        if not s:
            return "No drugstores or pharmacies were found for your query."
        
        final_output = llm.invoke(f"{s}<----Structure and present beautifully to the user")
        return str(final_output.content)

    return None
 # Let app.py handle normal queries





