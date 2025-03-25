from flask import Flask, render_template, redirect, url_for, request, flash, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')
DATABASE = 'meditrack.db'
ADMIN_DATABASE = 'adminbase.db'


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Patient (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL, 
                date_of_birth TEXT NOT NULL,
                pesel TEXT NOT NULL,    
                medical_history TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Appointment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                date_time TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES Patient (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL
            )
        ''')
        conn.commit()


def init_admin_db():
    with sqlite3.connect(ADMIN_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('SELECT COUNT(*) FROM Admin')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO Admin (username, password) VALUES (?, ?)', ('Test', 'Test'))
        conn.commit()


@app.before_first_request
def create_tables():
    init_db()
    init_admin_db()


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_admin_db_connection():
    conn = sqlite3.connect(ADMIN_DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def validate_admin(username, password):
    with get_admin_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Admin WHERE username = ? AND password = ?', (username, password))
        return cursor.fetchone()


def get_all_patients():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Patient')
        return cursor.fetchall()


def get_all_appointments():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Appointment')
        return cursor.fetchall()


def add_patient(name, date_of_birth, medical_history):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Patient (name, date_of_birth, medical_history) VALUES (?, ?, ?)',
                       (name, date_of_birth, medical_history))
        conn.commit()


def add_appointment(patient_id, date_time):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Appointment (patient_id, date_time) VALUES (?, ?)',
                       (patient_id, date_time))
        conn.commit()


def cancel_appointment(appointment_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Appointment WHERE id = ?', (appointment_id,))
        conn.commit()


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_patient', methods=['POST'])
def add_patient_route():
    if 'admin_id' in session:
        if request.method == 'POST':
            name = request.form['name']
            surname = request.form['surname']
            date_of_birth = request.form['date_of_birth']
            pesel = request.form['pesel']
            add_patient(name, surname, date_of_birth, pesel)
            flash('Patient added successfully !', 'success')
            return redirect(url_for('admin_panel'))
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        date_of_birth = request.form['date_of_birth']
        pesel = request.form['pesel']
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/schedule_appointment', methods=['GET', 'POST'])
def schedule_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        date_time = request.form['date_time']
        add_appointment(patient_id, date_time)
        flash('Appointment scheduled successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('schedule_appointment.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = validate_admin(username, password)
        if admin:
            session['admin_id'] = admin['id']
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('admin_login.html')


@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/admin_panel')
def admin_panel():
    if 'admin_id' in session:
        patients = get_all_patients()
        appointments = get_all_appointments()
        return render_template('admin_panel.html', patients=patients, appointments=appointments)
    else:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))



@app.route('/cancel_appointment/<int:appointment_id>')
def cancel_appointment_route(appointment_id):
    if 'admin_id' in session:
        cancel_appointment(appointment_id)
        flash('Appointment canceled successfully!', 'success')
        return redirect(url_for('admin_panel'))
    else:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)