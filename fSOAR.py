from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
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
    
    pass

@app.before_first_request
def initialize_app():
    initialize_database()

@app.route('/incident', methods=['POST'])
def handle_incident():
    incident = request.json

    if incident['type'] == 'alert':
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

        response = {
            'status': 'success',
            'message': 'Alert fired ',
            'incident': {
                'id': incident_id,
                'timestamp': incident['timestamp'],
                'type': incident['type'],
                'message': incident['message']
            }
        }
        send_qradar_request(response)

        # Incident report
        send_notification(incident)

        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO logs (timestamp, incident_type, message) VALUES (?, ?, ?)"
        values = (incident['timestamp'], incident['type'], 'Alert alındı ve işlendi.')
        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify(response), 200
    else:
        response = {
            'status': 'error',
            'message': 'Geçersiz olay türü.'
        }
        return jsonify(response), 400

@app.route('/add_action', methods=['POST'])
def add_action():
    data = request.json
    action = data['action']
    incident_id = data['incidentId']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Saving the action to database
    sql = "INSERT INTO actions (incident_id, action) VALUES (?, ?)"
    values = (incident_id, action)
    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    response = {
        'status': 'success',
        'message': 'Aksiyon başarıyla eklendi.'
    }
    return jsonify(response), 200


@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.json
    note = data['note']
    incident_id = data['incidentId']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Saving the incident note to database
    sql = "INSERT INTO notes (incident_id, note) VALUES (?, ?)"
    values = (incident_id, note)
    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    response = {
        'status': 'success',
        'message': 'Not başarıyla eklendi.'
    }
    return jsonify(response), 200

def send_notification(incident):
    pass

if __name__ == '__main__':
    app.run()
