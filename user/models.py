from pydoc import doc
from flask import Flask, jsonify, request, session, redirect,render_template
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return redirect('/pdashboard/')

  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.users.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    user = db.users.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401

  def symptoms(self):
    advice = {
      "name" : session['user']['name'],
      "_id" : session['user']['_id'],
      "Advice": True,
      "Doctor" : request.form.get('doctor'),
      "Symptom1": request.form.get('s1'),
      "Symptom2": request.form.get('s2'),
      "Symptom3": request.form.get('s3')
    }

    d = db.doctors.find_one({
      "name": advice['Doctor']
    })
    advice['d_id'] = d['_id']
    if db.questions.insert_one(advice):
      return redirect('/pdashboard')

# get advices//precription from doctor
  def advices(self):
    pass 

class Doctor:

  def start_session(self, doc):
    del doc['password']
    session['logged_in'] = True
    session['doc'] = doc
    return redirect('/ddashboard/')

  def signup(self):
    print(request.form)

    # Create the user object
    doc = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }

    # Encrypt the password
    doc['password'] = pbkdf2_sha256.encrypt(doc['password'])

    # Check for existing email address
    if db.doctors.find_one({ "email": doc['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.doctors.insert_one(doc):
      return self.start_session(doc)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    doc = db.doctors.find_one({
      "email": request.form.get('email')
    })

    if doc and pbkdf2_sha256.verify(request.form.get('password'), doc['password']):
      return self.start_session(doc)
    
    return jsonify({ "error": "Invalid login credentials" }), 401