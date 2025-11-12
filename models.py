from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ======== User ========


class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, autoincrement=True)
  email = Column(String, unique=True, nullable=False)
  password = Column(String, nullable=False)
  type = Column(String)  # 'admin', 'doctor', 'patient'

  admin = relationship('Admin', back_populates='user', uselist=False)
  doctor = relationship('Doctor', back_populates='user', uselist=False)
  patient = relationship('Patient', back_populates='user', uselist=False)


# ======== Admin ========

class Admin(db.Model):
  __tablename__ = 'admins'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  phone_num = Column(String)
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship('User', back_populates='admin')


# ======== Department ========

class Department(db.Model):
  __tablename__ = 'departments'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  description = Column(String)
  doctors = relationship('Doctor', back_populates='department')


# ======== Doctor ========

class Doctor(db.Model):
  __tablename__ = 'doctors'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  phone_num = Column(String)
  dept_id = Column(Integer, ForeignKey('departments.id'))
  user_id = Column(Integer, ForeignKey('users.id'))

  user = relationship('User', back_populates='doctor')
  department = relationship('Department', back_populates='doctors')
  appointments = relationship('Appointment', back_populates='doctor')


# ======== Patient ========

class Patient(db.Model):
  __tablename__ = 'patients'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  phone_num = Column(String)
  dob = Column(Date)
  user_id = Column(Integer, ForeignKey('users.id'))

  user = relationship('User', back_populates='patient')
  appointments = relationship('Appointment', back_populates='patient')


# ======== Appointment ========

class Appointment(db.Model):
  __tablename__ = 'appointments'
  id = Column(Integer, primary_key=True, autoincrement=True)
  patient_id = Column(Integer, ForeignKey('patients.id'))
  doctor_id = Column(Integer, ForeignKey('doctors.id'))
  date = Column(Date)
  time = Column(Time)
  status = Column(String, default='pending')  # pending, scheduled, completed

  patient = relationship('Patient', back_populates='appointments')
  doctor = relationship('Doctor', back_populates='appointments')
  treatment = relationship('Treatment', back_populates='appointment', uselist=False)


# ======== Treatment ========

class Treatment(db.Model):
  __tablename__ = 'treatments'
  id = Column(Integer, primary_key=True, autoincrement=True)
  appointment_id = Column(Integer, ForeignKey('appointments.id'), unique=True)
  diagnosis = Column(String)
  prescription = Column(String)
  notes = Column(String)
  tests = Column(String)

  appointment = relationship('Appointment', back_populates='treatment')
