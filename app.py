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

    return jsonify({"status": "success", "message": "Chấm công thành công"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5050)
