from flask import Flask, render_template, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# 🔹 Kết nối MongoDB (sửa lại MONGO_URI cho đúng của bạn)
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority"
)
DB_NAME = os.getenv("DB_NAME", "Sun_Database_1")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["HR_GPS_Attendance"]

# 🔹 Trang chính hiển thị bảng
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 API trả dữ liệu dạng JSON
@app.route("/api/attendances")
def get_attendances():
    try:
        data = list(collection.find({}, {"_id": 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
