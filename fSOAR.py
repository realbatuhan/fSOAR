from flask import Flask, request, jsonify
import sqlite3
import threading
import time

app = Flask(__fSoar__)
DATABASE = 'fsoar.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP NOT NULL,
            type TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id INTEGER,
            action TEXT NOT NULL,
            FOREIGN KEY (incident_id) REFERENCES incidents (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id INTEGER,
            note TEXT NOT NULL,
            FOREIGN KEY (incident_id) REFERENCES incidents (id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# QRadar API req. 
def send_qradar_request(data):
    # Implementation for sending a request to QRadar API
    pass

def sync_with_qradar():
    while True:
        # Fetch new incidents from QRadar
        new_incidents = fetch_new_incidents_from_qradar()

        # Process new incidents and send them to the frontend
        for incident in new_incidents:
            # Save incident to the database
            save_incident_to_database(incident)

            # Send incident to frontend
            send_incident_to_frontend(incident)

        # Wait for 2 seconds before the next synchronization
        time.sleep(2)

def fetch_new_incidents_from_qradar():
    # Implementation for fetching new incidents from QRadar API
    # You can replace this with your actual implementation
    return []

def save_incident_to_database(incident):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Database save function
    sql = "INSERT INTO incidents (timestamp, type, message) VALUES (?, ?, ?)"
    values = (incident['timestamp'], incident['type'], incident['message'])
    cursor.execute(sql, values)
    incident_id = cursor.lastrowid
    conn.commit()

    cursor.close()
    conn.close()

    # Send incident to QRadar
    send_qradar_request(incident)

def send_incident_to_frontend(incident):
    # Implementation for sending incident data to the frontend
    pass

@app.before_first_request
def initialize_app():
    initialize_database()
    # Start the synchronization thread
    sync_thread = threading.Thread(target=sync_with_qradar)
    sync_thread.start()

@app.route('/incident', methods=['POST'])
def handle_incident():
    # Your existing code for handling incidents
    pass

@app.route('/add_action', methods=['POST'])
def add_action():
    # Your existing code for adding actions
    pass

@app.route('/add_note', methods=['POST'])
def add_note():
    # Your existing code for adding notes
    pass

def send_notification(incident):
    # Your existing code for sending notifications
    pass

if __name__ == '__main__':
    app.run()
