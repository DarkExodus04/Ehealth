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
  user = session.get('user',None)
  doctors = list(db.doctors.find({},{'_id':0,'password': 0}))
  parameters = db.users.find_one({'_id':user['_id']},{'_id':0,'password': 0})
  return render_template('pdashboard.html',doctors = doctors, params = parameters)

@app.route('/symptoms/')
@login_required
def symptoms():
  doctors = list(db.doctors.find({},{'_id':0,'password': 0}))
  return render_template('symptoms.html',doctors = doctors)

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
#       print("Alert", "Converted Text: {}".format(text))
#     except:
#       print("ERROR","Could not recognize the voice")
      
#     values = listen(text)
#     print(values)
#     return render_template('voicepres.html', request="POST", values = values)
#   else:
#     return render_template("voicepres.html")

@app.route('/voicepres/', methods=['POST', 'GET'])
def voicepres():
  args = request.args
  patientid = args.get('id')
  parameters = db.parameters.find_one({'_id':patientid},{'_id':0,'password': 0})
  if request.method == "POST":
    f = request.data.decode("utf-8")
    js = json.loads(f)
    sentence = '. '.join(map(str,js))+'.'
    # values = listen(f)
    try:
      print("Alert", "Converted Text: {}".format(sentence))
    except:
      print("ERROR","Could not recognize the voice")
    pres = prescription(sentence)
    session['prescription'] = pres

    return render_template('voicepres.html', request="POST", parameters = parameters)
  else:
    return render_template("voicepres.html",parameters = parameters)

@app.route('/verify/')
def verify():
  pres = session.get('prescription',None)
  print(pres)
  return render_template('verify.html',pres = pres, s = "checked")

@app.route('/prescription/')
def prescription():
  dat = datetime.date.today()
  pres = session.get('prescription',None)
  return render_template('prescription.html',s = 'Dr. Nathan',pres = pres, date = dat)

@app.route('/doctorregister/')
def doctorregister():
  return render_template('doctorregister.html')

if __name__ == '__main__':
  os.environ['FLASK_ENV'] =  development
  app.run(debug = True)