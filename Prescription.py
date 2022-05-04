import nltk
from nltk.tag import StanfordNERTagger
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
stop_words = set(stopwords.words('english'))

import os
java_path = "C:/Program Files/Java/jdk-18.0.1/bin/java.exe"
os.environ['JAVAHOME'] = java_path

def prescription(inputPrescription):
# fetching all stops. Can edit all words from corpa of ntlk download  directory(generally home)
	top_words = set(stopwords.words('english')) 


	# inputPrescription = '''Diagnosis 1 pneumonia. Take Crocin 250 mg Injection before lunch after dinner for 2 days. Take Azithromycin after breakfast for 17 days. Take Salvin cold 1 mg Injection before dinner for 5 days. Advice 1 take steam. Advice 2 use warm cloths. stop'''
	inputPrescription = '''Diagnosis viral fever. take crocin 250 mg injection before lunch after lunch for 5 days. Take broncoTab tablet after dinner for 17 days. Take cefizox 1 mg injection before dinner for 5 days. Advice 1 take steam. Advice 2 use warm cloths. stop'''
	# words = inputPrescription.split()
	# new_words = []
	# for i in range(len(words)):

	# 	if words[i] == "take" or words[i] == "advice" or words[i] == "stop":
	# 	# 	new_words.append('. ')
	# 	# new_words.append(words[i])
	# 		words[i-1] = words[i-1] + '.'

	inputPrescription = ' '.join(map(str, words))
	print(inputPrescription)

	# for i in range(len(words)):
	# 	if words[i] == 'patient' or words[i] == 'diagnosis' or words[i] == 'advice' or words[i] == 'symptom':
	# 		words[i] = words[i].capitalize()
	# inputPrescription = ' '.join(map(str, words))
	# link to stanford engine and jar
	entity_tagger=StanfordNERTagger('C:/Nathan/Projects/GitHub/Ehealth/stanford-ner-tagger/v3_ner_model.ser.gz', 'C:/Nathan/Projects/GitHub/Ehealth/stanford-ner-tagger/' + 'stanford-ner-3.9.2.jar')

	#tokenize the sentences
	tokens = nltk.word_tokenize(inputPrescription)

	#use NER tagger on tokens
	data = entity_tagger.tag(tokens)

	# Generating Prescription----------------------------------------------------------------


	patientID = 0
	patientName = ""
	Medicines = []
	DoseString = ["before breakfast", "after breakfast", "before lunch", "after lunch", "before dinner", "after dinner", "before sleeping"]
	Dose = []
	Diagnosis = []
	Symptom = []
	Advice = []
	Days = []

	i = 0
	while i < len(data):
		print(str(i) + "\t" + data[i][0] + " " + data[i][1])
		#checking for user details
		if data[i][1] == 'STP':
			break
		elif data[i][1] == 'USER':

			#checking if next word is id
			if data[i+1][1] == 'TAG':
				#skipping 'patient', 'is' and 'id'
				patientID = data[i+3][0]
				print("Patient ID: " + str(patientID))
				i += 4

			#checking if next word is name
			elif data[i+1][0] == 'name':
				#concatenating till dot found
				DOTi = i+3
				while data[DOTi+1][1] != 'DOT':
					patientName += data[DOTi][0] + " "
					DOTi += 1
				patientName += data[DOTi][0]
				print("Patient Name: " + patientName)
				i += 4
		
		#checking for medicines
		elif data[i][1] == 'MED':
			#found take and adding name of med after take till TIM tag
			TIMi = i+1
			medicinename = ""
			try:
				while data[TIMi+1][1] != 'TIM':
					medicinename += data[TIMi][0] + " "
					TIMi += 1
			except:
				break
			medicinename += data[TIMi][0]
			Medicines.append(medicinename)
			i = TIMi
		
		elif data[i][1] == 'TIM':
			DOTi = i
			MDose = [0,0,0,0,0,0,0]
			while data[DOTi][1] != 'DOT':
				if data[DOTi][0] != 'and' and data[DOTi][0] != 'days':
					print("Next Element:" + data[DOTi][0])
					dose = data[DOTi][0] + " " + data[DOTi+1][0]
					print(dose)
					itr = 0
					while itr < len(DoseString):
						print("calculating" + str(itr) + " " + dose + " " + DoseString[itr])
						if DoseString[itr] == dose:
							MDose[itr] = 1
							break
						itr += 1
					DOTi += 1
				else:
					Days.append(data[DOTi-1][0])
					print("\t" + str(Days))
					DOTi += 1
					print(data[DOTi][0])
					break
			Dose.append(MDose)
			i = DOTi

		elif data[i][1] == 'SYM':
			sym = ""
			DOTi = i+1
			while data[DOTi+1][1] != 'DOT':
				sym += data[DOTi][0] + " "
				DOTi += 1
			sym += data[DOTi][0] +"."
			Symptom.append(sym)
			i = DOTi
			#print(data[i][0])

		elif data[i][1] == 'DIA':
			dia = ""
			DOTi = i+1
			while data[DOTi+1][1] != 'DOT':
				dia += data[DOTi][0] + " "
				DOTi += 1
			dia += data[DOTi][0] +"."
			Diagnosis.append(dia)
			i = DOTi
			#print(data[i][0])


		elif data[i][1] == 'ADC':
			adc = ""
			DOTi = i+1
			while data[DOTi+1][1] != 'DOT':
				adc += data[DOTi][0] + " "
				DOTi += 1
			adc += data[DOTi][0] +"."
			Advice.append(adc)
			i = DOTi

		i += 1

	# print(Medicines)
	# print(Dose)

	print(Symptom)
	print(Diagnosis)
	print(Advice)

	print("\t\n\n\n---------------------------Prescription------------------------------\n")
	print("\tPatient Name:  " + patientName + "")
	print("\tPatient ID:  " + str(patientID) + "\n\n")

	print("MEDICINES:")
	i = 0
	while i < len(Medicines):
		print("\t" + Medicines[i])
		print("\t  " + "for " + str(Days[i]) + "days")
		itr = 0
		while itr < 7:
			if Dose[i][itr] == 1:
				print("\t\t" + DoseString[itr])
			itr += 1
		i += 1
		print("\n")

	print("\nDIAGONSIS:")
	l = 0
	while l < len(Diagnosis):
		print("\t" + Diagnosis[l])
		l += 1

	print("\nSYMPTOMS:")
	j = 0
	while j < len(Symptom):
		print("\t" + Symptom[j])
		j += 1

	print("\nADVICE:")
	k = 0
	while k < len(Advice):
		print("\t" + Advice[k])
		k += 1

	print("\n------------------------------------------------------------------------")

	data_json = {}
	data_json["PatientName"] = patientName
	data_json["PatientID"] = patientID
	data_json["Age"] = 20
	data_json["Medicines"] = Medicines
	data_json["Dose"] = Dose
	data_json["Days"] = Days
	data_json["Symptom"] = Symptom 
	data_json["Diagnosis"] = Diagnosis
	data_json["Advice"] = Advice
	return data_json
