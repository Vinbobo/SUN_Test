from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_cors import CORS
from pymongo import MongoClient
import os, requests

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://banhbaobeo2205:lm2hiCLXp6B0D7hq@cluster0.festnla.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.getenv("DB_NAME", "Sun_Database_1")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["HR_GPS_Attendance"]

# Hàm reverse geocoding như trước
def get_address_from_latlng(lat, lng):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"format": "json", "lat": lat, "lon": lng, "zoom": 18, "addressdetails": 1}
    headers = {"User-Agent": "gps-checkin-app"}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("display_name", "")
    except Exception as e:
        print("Reverse geocoding error:", e)
    return ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/records")
def records():
    return render_template("records.html")

@app.route("/api/checkin", methods=["POST"])
def checkin():
    data = request.get_json()
    emp_id = data.get("EmployeeId")
    emp_name = data.get("EmployeeName")
    lat = data.get("Latitude")
    lng = data.get("Longitude")
    address = get_address_from_latlng(lat, lng) if lat and lng else ""

    checkin_data = {
        "EmployeeId": emp_id,
        "EmployeeName": emp_name,
        "Latitude": lat,
        "Longitude": lng,
        "Address": address or "Không xác định",
        "CheckinTime": datetime.now(),
        "Status": "Checked In"
    }
    collection.insert_one(checkin_data)

    return jsonify({"message": "Điểm danh thành công!", "address": address or "Không xác định"})

@app.route("/api/attendances", methods=["GET"])
def get_attendances():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
