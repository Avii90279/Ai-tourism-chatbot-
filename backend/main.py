from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from deep_translator import GoogleTranslator
import requests


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 Your API Keys
GEMINI_API_KEY = "AIzaSyBUt2Fd3In9Zvs5qbdEDeij63vQiFA3KW8"
WEATHER_API_KEY = "e723328c7a4acbefd534bba4bd006d50"
GOOGLE_MAPS_API_KEY = "AIzaSyBPF9Tb_Gz7ph4KWBggs_1IGxIrMpTzUPc"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")


def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()
        if res["cod"] == 200:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"].capitalize()
            humidity = res["main"]["humidity"]
            wind = res["wind"]["speed"]
            return f"🌦️ Weather in {city}: {temp}°C, {desc}, Humidity: {humidity}%, Wind: {wind} m/s."
        else:
            return "⚠️ Weather data not found for that city."
    except:
        return "⚠️ Unable to fetch weather details right now."

def get_maps_link(city):
    return f"https://www.google.com/maps/embed/v1/place?q={city}&key={GOOGLE_MAPS_API_KEY}"

# ---------------- CHATBOT ----------------
@app.get("/chat")
def chat(query: str, lang: str = "en"):
    try:
        # Translate query to English
        query_en = query if lang == "en" else GoogleTranslator(source='auto', target='en').translate(query)

        # Gemini prompt
        prompt = f"""
        You are a friendly AI tourism chatbot for India.
        If the user mentions a city or tourist place, respond with:
        - Short travel description
        - Mention attractions
        - Suggest best time to visit
        - Be warm and human-like.
        Also, if user just chats normally, respond casually.
        User: {query_en}
        """
        response = model.generate_content([prompt])
        reply = response.text

        # Detect city name
        words = query_en.split()
        city = None
        for w in words:
            if w[0].isupper() and len(w) > 2:
                city = w
                break

        weather_info = get_weather(city) if city else ""
        map_link = get_maps_link(city) if city else ""

        # Translate reply and weather back
        if lang != "en":
            reply = GoogleTranslator(source='en', target=lang).translate(reply)
            weather_info = GoogleTranslator(source='en', target=lang).translate(weather_info)

        return {
            "reply": reply,
            "weather": weather_info,
            "map_url": map_link
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "🌍 Tourism Chatbot with Maps & Weather is live!"}
