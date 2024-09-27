from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit
import random
import threading
import time
from flask_cors import CORS

app = Flask(__name__, static_folder='dist/site-device-dashboard/browser')
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
# Initialize SocketIO with ping_timeout and ping_interval
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=120, ping_interval=25)
# --- Node.js Converted Code ---
# Sample tank data
tank_data = [
    {
        "title": "Tank 1",
        "type": "Unleaded",
        "alertStatus": "0",
        "fillPercentage": 50,
        "waterFillPercentage": 20,
        "capacity": 200,
        "volume": 100,
    },
    {
        "title": "Tank 2",
        "type": "Diesel",
        "alertStatus": "1",
        "fillPercentage": 60,
        "waterFillPercentage": 30,
        "capacity": 300,
        "volume": 200,
    },
    {
        "title": "Tank 3",
        "type": "Octane 91",
        "alertStatus": "0",
        "fillPercentage": 80,
        "waterFillPercentage": 20,
        "capacity": 400,
        "volume": 380,
    },
    {
        "title": "Tank 4",
        "type": "Petrol",
        "alertStatus": "0",
        "fillPercentage": 30,
        "waterFillPercentage": 20,
        "capacity": 400,
        "volume": 150,
    },
    {
        "title": "Tank 5",
        "type": "Regular",
        "alertStatus": "0",
        "fillPercentage": 80,
        "waterFillPercentage": 20,
        "capacity": 400,
        "volume": 400,
    },
    {
        "title": "Tank 6",
        "type": "Premium",
        "alertStatus": "0",
        "fillPercentage": 65,
        "waterFillPercentage": 15,
        "capacity": 200,
        "volume": 150,
    },
]

# Sample site data
sites = [
    {
        "id": 1,
        "title": "Fuel Controller",
        "lastUpdated": "3 min ago",
        "dynamicText": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "details": [
            {"key": "VM Status", "value": "Active"},
            {"key": "Services", "value": "Stopped"},
        ],
    },
    {
        "id": 2,
        "title": "Site Controller",
        "lastUpdated": "4 min ago",
        "dynamicText": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "details": [
            {"key": "VM Status", "value": "Active"},
            {"key": "Services", "value": "Stopped"},
            {"key": "Alerts", "value": "None"},
        ],
    },
    {
        "id": 3,
        "title": "POS",
        "lastUpdated": "1 min ago",
        "dynamicText": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "details": [
            {"key": "VM Status", "value": "Active"},
            {"key": "Services", "value": "Stopped"},
        ],
    },
    {
        "id": 4,
        "title": "EPC Controller",
        "lastUpdated": "4 min ago",
        "dynamicText": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
        "details": [
            {"key": "VM Status", "value": "Active"},
            {"key": "Services", "value": "Stopped"},
            { "key": "SAF Count", "value": "20" },
            { "key": "SAF Amount", "value": "100" },
            { "key": "Host Status", "value": "Active" },
        ],
    }
]

# Sample pump status data
pump_status_list = [
    {"id": 1, "title": "Gilbarco - FPI", "printerStatus": "Printer status", "status": "Idle"},
    {"id": 2, "title": "FPI 2", "printerStatus": "Printer status", "status": "Payment"},
    {"id": 3, "title": "FPI 3", "printerStatus": "Printer status", "status": "Offline"},
    {"id": 4, "title": "FPI 4", "printerStatus": "Printer status", "status": "Idle"},
    {"id": 5, "title": "Gilbarco - FPI 5", "printerStatus": "Printer status", "status": "Offline"},
    {"id": 6, "title": "FPI 6", "printerStatus": "Printer status", "status": "Fuelling"},
]

# Sample price status data
price_status_list = [
    {"name": "Petrol", "pump": 234.00, "pole": 233.00},
    {"name": "Diesel", "pump": 234.00, "pole": 233.00},
    {"name": "Grade 1", "pump": 234.00, "pole": 233.00},
    {"name": "Grade 2", "pump": 234.00, "pole": 233.00},
    {"name": "Grade 3", "pump": 234.00, "pole": 233.00},
]

# When a client connects to the Socket.IO server
@socketio.on("connect")
def handle_connect():
    print("A client connected")
    emit("tankData", tank_data)

# Function to simulate updating tank data
def update_tank_data():
    while True:
        for tank in tank_data:
            tank["fillPercentage"] = random.randint(0, 80)
        #print("Emitting tank data:", tank_data)  # Add this line to log the data
        socketio.emit("tankData", tank_data)
        time.sleep(10)

# Background thread to update tank data
def start_background_thread():
    thread = threading.Thread(target=update_tank_data)
    thread.daemon = True
    thread.start()

# Start the background thread when the server starts
start_background_thread()

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

# API Endpoint 1: Returns an array of tank data
@app.route("/api/tankData", methods=['GET'])
def get_tank_data():
    return jsonify(tank_data)

# API Endpoint 2: Returns an array of site data
@app.route("/api/siteList", methods=['GET'])
def get_site_data():
    return jsonify(sites)

# API Endpoint 3: Returns an array of pump status data
@app.route("/api/pumpStatusList", methods=['GET'])
def get_pump_status_data():
    return jsonify(pump_status_list)

# API Endpoint 4: Returns an array of price status data
@app.route("/api/priceList", methods=['GET'])
def get_price_status_data():
    return jsonify(price_status_list)



# --- Original Python Code ---
# Sample data for notifications and devices
notifications = ["System started", "New device connected"]
actions = ["Check device status", "Review logs"]

devices = [
    {"id": 1, "name": "Site Controller", "status": "active"},
    {"id": 2, "name": "EPC", "status": "active"},
    {"id": 3, "name": "Pump Controller", "status": "active"},
    {"id": 4, "name": "FP1", "status": "active", "current_price": {"grade1": "2", "grade2": "2.5"}},
    {"id": 5, "name": "FP2", "status": "active", "current_price": {"grade1": "2", "grade2": "2.5"}},
    {"id": 6, "name": "FP3", "status": "inactive", "current_price": {"grade1": "2", "grade2": "2.5"}},
    {"id": 7, "name": "FP4", "status": "active", "current_price": {"grade1": "2", "grade2": "2.5"}},
    {"id": 8, "name": "FP5", "status": "inactive", "current_price": {"grade1": "2", "grade2": "2.5"}},
    {"id": 9, "name": "FP6", "status": "active", "current_price": {"grade1": "2", "grade2": "2.5"}}
]

@app.route('/devices')
def get_devices():
    return jsonify(devices)

def start_flask_server():
    socketio.run(app, debug=True, use_reloader=False)

def notify_clients(data):
    socketio.emit('update', data)
    socketio.emit('update', {
            'notifications': notifications,
            'actions': actions
        })

def stop_flask_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# --- Main Entry Point ---
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=3000, debug=True)

