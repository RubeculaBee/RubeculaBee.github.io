from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS, cross_origin
from google import genai
from google.genai import types
from werkzeug.utils import secure_filename
from pydantic import BaseModel
import json
import os.path
import whisper

UPLOAD_FOLDER = 'upload'

class studyInfo(BaseModel):
	topic: str
	keyPoints: list[str]
	exampleProblem: list[str]

class questionStructure(BaseModel):
    question: str
    answers: list[str]
    correct: int

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

#This defines the default root
@app.route("/")
def uploadPage():
    return render_template('upload.html')
    
@app.route("/connect", methods=['GET'])
def connectToPage():
	
	#Put code here that checks if api file is here!
	
	#Prints out a simple boolean if the file does not exist!
	fileExists = os.path.isfile("apikey.txt")
	
	if(fileExists is False):
		response = jsonify({'keyFound': 0}) #No Key was found!
	else:
		#Add code to see if file is populated!
		response = jsonify({'keyFound': 1}) #Key was found!
	#response.headers.add("Access-Control-Allow-Origin", "*")
	
	#return render_template('upload.html')
	
	return response, 200
	
@app.route("/createAPIKey", methods=['POST'])
def createKey():
	data = request.json
	print(data)
	
	f = open("apikey.txt", "w")
	f.write(data["key"])
	f.close()
	
	response = jsonify({'keyUploaded': 1})
	
	return response, 200
	
@app.route("/question", methods=['POST'])
def askQuestion():
	
	#Open API key file
	f = open("apikey.txt", "r")
	key = f.read()
	f.close()
    
    #Open transcript file
	f = open("transcript.txt", "r")
	transcription = f.read()
	f.close()
	
	data = request.json
	
	#userQuestion = "I am giving you the transcript of a lecture. When you summarize the following transcript, I want you to pull out specifc information and sort them into sections. The first section should be a single sentence description of the topic of the lecture. The second section should be the key points taught in the lecture. The third section should be an example of a problem that was taught in the lecture, and you should work through that problem step by step. Your response should come in the form of a JSON file. Summarize this: " + transcription
	userQuestion = "Summarize this transcript of a lecture. Please make sure to return information about the lecture's overall TOPIC, KEY POINTS from the lecture, and an example problem (if present in transcription) discussed and explained in a step-by-step manner: " + transcription
	userInstruction = data["instruction"]
	
	client = genai.Client(api_key=key)
	
	response = client.models.generate_content(
    model="gemini-2.0-flash",
    config={
		'response_mime_type': 'application/json',
		'response_schema': studyInfo,
	},
    contents=userQuestion,
	)
	
	out = response.text
	
	print(out)
	
	response = jsonify({'answer': out})
	
	return response, 200
	
@app.route("/makeQuiz", methods=['GET'])
def makequiz():
    print("open key")
    #Open API key file
    f = open("apikey.txt", "r")
    key = f.read()
    f.close()
    
    print("open transcript")
    #Open transcript file
    f = open("transcript.txt", "r")
    transcription = f.read()
    f.close()
    
    print("get client")
    client = genai.Client(api_key=key)
    
    print("get prompt")
    userQuestion = "You will be provided with the transcript of a lecture. Design a multiple choice quiz question based on the topic of the lecture. There should be 4 answers, of which 1 is correct and the other 3 are wrong. You will provide the number of the answer that is correct. Here is the transcript: " + transcription
    
    print("generate response")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config={
            'response_mime_type': 'application/json',
            'response_schema': questionStructure
        },
        contents=userQuestion
    )
    print(response.text)
    
    print("jsonify response")
    response = jsonify({'answer': response.text})
    
    print("return response")
    return response, 200

	
@app.route("/saveFile", methods=['POST'])
def saveFile():
    file = request.files['file']
    filename = 'audio'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    print("transcribe file")
	
    model = whisper.load_model("tiny.en")
    result = model.transcribe(os.path.join(app.config['UPLOAD_FOLDER'], 'audio'))
    
    f = open("transcript.txt", "w")
    f.write(result['text'])
    f.close()
    
    response = jsonify({'message': "File Uploaded!"})
    return response, 200

    
if __name__ == '__main__':
	app.run()
