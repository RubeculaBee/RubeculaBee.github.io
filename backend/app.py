from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from google import genai
from google.genai import types
from werkzeug.utils import secure_filename
import json
import os.path
import whisper

UPLOAD_FOLDER = 'upload'

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
	
	data = request.json
	
	userQuestion = data["question"]
	userInstruction = data["instruction"]
	
	client = genai.Client(api_key=key)
	
	response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
		system_instruction=userInstruction),
    contents=userQuestion
	)
	
	out = response.text
	
	response = jsonify({'answer': out})
	
	return response, 200
	
	
	
	
@app.route("/transcribeAudio", methods=['POST'])
def transcribeAudio():
    file = request.files['file']
    filename = 'audio'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    #model = whisper.load_model("tiny.en")
    #result = model.transcribe(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    #print(result['text'])
    
    response = jsonify({'message': "File Uploaded!"})
    return response, 200

    
if __name__ == '__main__':
	app.run()
