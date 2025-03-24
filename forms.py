from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    medical_history = TextAreaField('Medical History')
    submit = SubmitField('Add Patient')

class AppointmentForm(FlaskForm):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    date_time = StringField('Date and Time (YYYY-MM-DD HH:MM)', validators=[DataRequired()])
    submit = SubmitField('Schedule Appointment')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')