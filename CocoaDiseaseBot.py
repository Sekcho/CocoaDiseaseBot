from flask import Flask, request
import requests

# Configuration
TELEGRAM_BOT_TOKEN = "8088237394:AAGspAq0hDF7aCV_rhcmRrC95xAo4rSnbk8"
OPENWEATHERMAP_API_KEY = "f1444b5043cbba89d9464339f54884f7"
LOCATION_LAT = "7.3064365"
LOCATION_LON = "100.2438508"

# Initialize Flask app
app = Flask(__name__)

# Route for root URL
@app.route("/")
def index():
    return "Telegram Bot is running!", 200

# Function to get weather data
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={LOCATION_LAT}&lon={LOCATION_LON}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Route to handle Telegram updates
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            message = "ยินดีต้อนรับ! ใช้คำสั่ง /weather เพื่อดูข้อมูลสภาพอากาศ 🌦️"
        elif text == "/weather":
            weather_data = get_weather()
            if weather_data:
                temp = weather_data["main"]["temp"]
                description = weather_data["weather"][0]["description"]
                message = f"🌡️ อุณหภูมิ: {temp}°C\n🌤️ สภาพอากาศ: {description.capitalize()}"
            else:
                message = "❌ ไม่สามารถดึงข้อมูลสภาพอากาศได้ในขณะนี้"
        else:
            message = "คำสั่งไม่ถูกต้อง! ใช้ /start หรือ /weather"

        send_telegram_message(chat_id, message)

    return "OK", 200
  # ตอบกลับไปยัง Telegram ว่ารับคำขอแล้ว

# Function to send message via Telegram
def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    print("Message sent response:", response.json())  # Debug ผลลัพธ์

# Add header to skip ngrok browser warning
@app.after_request
def add_header(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

# Log incoming requests for debugging
@app.before_request
def log_request():
    print(f"Incoming request: {request.method} {request.url}")

if __name__ == "__main__":
    app.run(port=5000)
