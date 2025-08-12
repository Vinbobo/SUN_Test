from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime
from flask_cors import CORS  # <- thêm dòng này

app = Flask(__name__)
CORS(app)  # <- thêm dòng này để cho phép CORS
# ⚙️ Kết nối SQL Server
conn_str = (
    "Driver={SQL Server};"
    "Server=DESKTOP-LF6CHGA\\SQLEXPRESS;"
    "Database=Sun_Database;"
    "Trusted_Connection=yes;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

@app.route("/api/checkin", methods=["POST"])
def checkin():
    data = request.get_json()
    emp_id = data.get("EmployeeId")
    emp_name = data.get("EmployeeName")
    latitude = data.get("Latitude")
    longitude = data.get("Longitude")
    time_now = datetime.now()

    if not all([emp_id, emp_name, latitude, longitude]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    query = """
        INSERT INTO HR_GPS_Attendance (EmployeeId, EmployeeName, CheckInTime, Latitude, Longitude)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (emp_id, emp_name, time_now, latitude, longitude))
    conn.commit()
import os
from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sử dụng driver ODBC cho Linux
conn_str = os.getenv(
    "SQLSERVER_CONN_STR",
    "Driver={ODBC Driver 18 for SQL Server};Server=your_server.database.windows.net,1433;Database=Sun_Database;Uid=render_user;Pwd=StrongPassword123!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

@app.route("/")
def health():
    return "OK", 200

@app.route("/api/checkin", methods=["POST"])
def checkin():
    data = request.get_json()
    emp_id = data.get("EmployeeId")
    emp_name = data.get("EmployeeName")
    latitude = data.get("Latitude")
    longitude = data.get("Longitude")
    time_now = datetime.now()

    if not all([emp_id, emp_name, latitude, longitude]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    query = """
        INSERT INTO HR_GPS_Attendance (EmployeeId, EmployeeName, CheckInTime, Latitude, Longitude)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (emp_id, emp_name, time_now, latitude, longitude))
    conn.commit()

    return jsonify({"status": "success", "message": "Chấm công thành công"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
