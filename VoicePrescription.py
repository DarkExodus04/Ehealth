import speech_recognition as sr
import os
from extract_text import extract
from create_document import create
from send_mail import upload


#send mail
# def verify(name=None):
# 	# To open files redirected form other function after creation
# 	if name:
# 		p = "F:/Mini Projects Rishi/voice prescription/{}.docx".format(name)
# 	# Manual verification of existing files
# 	else:
# 		filename = filedialog.askopenfilename(initialdir="C:\\Nathan\\Projects\\GitHub\\Voice-Prescription", title="Select file", filetypes=(("document files", "*.docx"), ("all files", "*.*")))
# 		p = filename

# 	# Split path and file name
# 	a = os.path.split(p)
# 	try:
# 		# Opens file
# 		os.startfile(a[0] + '/' + a[1])
# 		sleep(10)
# 		# Call upload function to send prescription through mail
# 		upload(p)
# 	except:
# 		print("ERROR", "Could not open file")

def listen():
	#Microphone
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Alert", "Start Speaking")
		audio = r.listen(source, timeout = 4)
	
	#test voice
	# r = sr.Recognizer()
	# try:
	# 	with sr.AudioFile('test-voice.wav') as source:
	# 		audio = r.listen(source)
	# except:
	# 	print("ERROR","Could not open file, please select .wav file")


	# Convert audio to text
	try:
		text = r.recognize_google(audio)
		print("Alert", "Converted Text: {}".format(text))
	except:
		print("ERROR","Could not recognize the voice")
	
	# Extract text
	try:
		name, age, date, tablet = extract(text)

		print(name,age,tablet)
	except ValueError:
	 	print("ERROR","Could not find patient Name")
	# except:
	#  	print("ERROR","Could not extract text")
	
	# # Create document
	try:
		create(name, age, date, tablet)
	except PermissionError:
		print("ERROR","The document is open, please close and try again!")
	except:
		print("ERROR","Could not create document")

	# # Verify document
	# try:
	# 	verify(name)
	# except:
	# 	print("ERROR","Could not open file")


listen()