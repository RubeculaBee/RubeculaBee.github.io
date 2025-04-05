from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os.path
import whisper

app = Flask(__name__)
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
	
	
@app.route("/transcribeAudio", methods=['POST'])
def transcribeAudio():
    data = request.json
    
    model = whisper.load_model("tiny.en")
    result = model.transcribe(data["file"])
    
    return result, 200
    
if __name__ == '__main__':
	app.run()
