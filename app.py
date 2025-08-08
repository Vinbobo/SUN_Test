
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from sqlalchemy import create_engine, text
import urllib

app = Flask(__name__)

# SQL Server connection config
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-LF6CHGA\SQLEXPRESS;"
    "DATABASE=Sun_Database;"
    "Trusted_Connection=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/checkin', methods=['POST'])
def checkin():
    data = request.json
    emp_id = data.get('EmployeeId')
    emp_name = data.get('EmployeeName')
    latitude = data.get('Latitude')
    longitude = data.get('Longitude')
    checkin_time = datetime.now()
    status = "Checked-in"

    query = text("""
        INSERT INTO HR_GPS_Attendance (EmployeeId, EmployeeName, CheckInTime, Latitude, Longitude, Status)
        VALUES (:emp_id, :emp_name, :checkin_time, :latitude, :longitude, :status)
    """)
    with engine.begin() as conn:
        conn.execute(query, {
            'emp_id': emp_id,
            'emp_name': emp_name,
            'checkin_time': checkin_time,
            'latitude': latitude,
            'longitude': longitude,
            'status': status
        })

    return jsonify({"message": "Check-in successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)
