from flask import Flask
from app import app
from user.models import User,Doctor

@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/user/signout')
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
  return User().login()

@app.route('/user/symptom', methods=['POST'])
def symptom():
  return User().symptoms()

@app.route('/doc/signup', methods=['POST'])
def dsignup():
  return Doctor().signup()

@app.route('/doc/signout')
def dsignout():
  return Doctor().signout()

@app.route('/doc/login', methods=['POST'])
def dlogin():
  return Doctor().login()