import sqlite3

DATABASE = 'meditrack.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def add_patient(name, surname, date_of_birth, pesel, medical_history=''):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Patient (name, surname, date_of_birth, pesel, medical_history) VALUES (?, ?, ?, ?, ?)',
                   (name, surname, date_of_birth, pesel, medical_history))
    conn.commit()
    conn.close()

def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Patient')
    patients = cursor.fetchall()
    conn.close()
    return patients

def add_appointment(patient_id, date_time):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Appointment (patient_id, date_time) VALUES (?, ?)', 
                   (patient_id, date_time))
    conn.commit()
    conn.close()

def get_appointments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Appointment')
    appointments = cursor.fetchall()
    conn.close()
    return appointments

def validate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user