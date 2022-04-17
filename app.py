from flask import Flask, render_template, session, redirect,request
from functools import wraps
import pymongo
from VoicePrescrip.VoicePrescription import listen
import speech_recognition as sr

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.ehealth

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/patientregister/')
def patientregister():
  return render_template('patientregister.html')

@app.route('/pdashboard/')
@login_required
def pdashboard():
  return render_template('pdashboard.html')

@app.route('/ddashboard/')
@login_required
def ddashboard():
  return render_template('ddashboard.html')


@app.route('/voicepres/', methods=['POST', 'GET'])
def voicepres():
  r = sr.Recognizer()
  if request.method == "POST":
    f = request.files['audio_data']
    print("Successfull")
    with open('audio.wav', 'wb') as audio:
        f.save(audio)
    with sr.AudioFile('audio.wav') as source:
      audio1 = r.listen(source)
    print('file uploaded successfully')

    try:
      text = r.recognize_google(audio1)
      print("Alert", "Converted Text: {}".format(text))
    except:
      print("ERROR","Could not recognize the voice")
      
    values = listen(text)
    print(values)
    return render_template('voicepres.html', request="POST", values = values)
  else:
    return render_template("voicepres.html")


@app.route('/doctorregister')
def doctorregister():
  return render_template('doctorregister.html')