from asyncio import QueueEmpty
from flask import Flask, render_template, session, redirect,request,url_for
from functools import wraps
import pymongo,os,json
from VoicePrescrip.VoicePrescription import listen
from Prescription import prescription
import speech_recognition as sr
import datetime

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
# client = pymongo.MongoClient('localhost',27017)
client = pymongo.MongoClient("mongodb+srv://ank:anchal@cluster0.cvjbn.mongodb.net/test")
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
  user = session.get('user',None)
  doctors = list(db.doctors.find({},{'_id':0,'password': 0}))
  parameters = db.parameters.find_one({'p_id':user['_id']},{'_id':0})
  return render_template('pdashboard.html',doctors = doctors, param = parameters['sensors'])

@app.route('/symptoms/')
@login_required
def symptoms():
  user = session.get('user',None)
  parameters = db.parameters.find_one({'p_id':user['_id']},{'_id':0})
  doctors = list(db.doctors.find({},{'_id':0,'password': 0}))
  return render_template('symptoms.html',doctors = doctors,param = parameters['sensors'])

@app.route('/ddashboard/')
@login_required
def ddashboard():
  doc = session.get('doc',None)
  patients = list(db.users.find({},{'password': 0}))
  questions = list(db.questions.find({'d_id':doc['_id']},{'_id' : 0,'d_id' : 0}))
  for patient in patients:
    for question in questions:
      if question['name'] == patient['name']:
        patient['Advice'] = question['name']
        patient['Symptom1'] = question['Symptom1']
        patient['Symptom2'] = question['Symptom2']
        patient['Symptom3'] = question['Symptom3']
  return render_template('ddashboard.html',patients = patients)


# @app.route('/voicepres/', methods=['POST', 'GET'])
# def voicepres():
#   r = sr.Recognizer()
#   if request.method == "POST":
#     f = request.files['audio_data']
#     print("Successfull")
#     with open('audio.wav', 'wb') as audio:
#         f.save(audio)
#     with sr.AudioFile('audio.wav') as source:
#       audio1 = r.listen(source)
#     print('file uploaded successfully')

#     try:
#       text = r.recognize_google(audio1)
#       print(text)
#       print("Alert", "Converted Text: {}".format(text))
#     except:
#       print("ERROR","Could not recognize the voice")
      
#     values = listen(text)
#     print(values)
#     return render_template('try.html', request="POST", values = values)
#   else:
#     return render_template("try.html")

@app.route('/voicepres/', methods=['POST', 'GET'])
def voicepres():
  args = request.args
  patientid = args.get('id')
  print(patientid)
  parameters = db.parameters.find_one({'p_id':patientid},{'_id':0})
  if request.method == "POST":
    # f = request.data.decode("utf-8")
    # js = json.loads(f)
    file = request.files['audio_data']
    if file.filename == "":
      return redirect(request.url)

    if file:
      recognizer = sr.Recognizer()
      audioFile = sr.AudioFile(file)
      with audioFile as source:
          data = recognizer.record(source)
      sentence = recognizer.recognize_google(data, key=None)
    # sentence = '. '.join(map(str,js))+'.'
    # values = listen(f)
    try:
      print("Alert", "Converted Text: {}".format(sentence))
    except:
      print("ERROR","Could not recognize the voice")
    pres = prescription(sentence)
    session['prescription'] = pres

    return render_template('voicepres.html', request="POST", param = parameters['sensors'], transcript = sentence)
  else:
    return render_template("voicepres.html",param = parameters['sensors'])

# @app.route('/voicepres/', methods=['POST', 'GET'])
# def voicepres():
#   transcript = ""
#   if request.method == "POST":
#     print("FORM DATA RECEIVED")
#     file = request.files['audio_data']

#     # if "file" not in request.files:
#     #   print('ua')
#     #   return redirect(request.url)

    
#     if file.filename == "":
#       print('u')
#       return redirect(request.url)

#     if file:
#       recognizer = sr.Recognizer()
#       audioFile = sr.AudioFile(file)
#       with audioFile as source:
#           data = recognizer.record(source)
#       transcript = recognizer.recognize_google(data, key=None)
#   print(transcript)
#   return render_template('try.html', transcript=transcript)

@app.route('/verify/')
def verify():
  pres = session.get('prescription',None)
  print(pres)
  return render_template('verify.html',pres = pres, s = "checked")

@app.route('/fprescription/')
def fprescription():
  dat = datetime.date.today()
  pres = session.get('prescription',None)
  return render_template('prescription.html',s = 'Dr. Nathan',pres = pres, date = dat)

@app.route('/doctorregister/')
def doctorregister():
  return render_template('doctorregister.html')

if __name__ == '__main__':
  os.environ['FLASK_ENV'] =  development
  app.run(debug = True)