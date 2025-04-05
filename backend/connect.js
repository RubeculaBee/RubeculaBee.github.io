const baseURL = "http://127.0.0.1:5000/connect";

//This is the basic connect function!
async function fetchUrlData(url, options = {}){
	const response = await fetch(url, options);
	
	
	if (!response.ok){
		return null;
	}
	
	//Expects the response to be in JSON
	const text = await response.text();
	return JSON.parse(text);
}


async function testConnection(){
	
	// Element that will display error message
	const errorMessage = document.getElementById("err");
	
	//let output = document.getElementById("status");
	
	//Try to connect to the server!
	try{
		//Run this code is server is running!
		data = await fetchUrlData(baseURL);
		//output.innerHTML = "Successfully connected!";
		
		console.log(data["keyFound"]);
		
		if(data["keyFound"]){ //If key is found!
			console.log("Key was found!");
			
		}else{ //If key is NOT found!
			console.log("Key Was not found!");
			window.location.replace("backend/noapikey.html");
		}
		
	} catch (error){
		//Add code here to redirect to put out error message saying not connected!
		//output.innerHTML = "NOT CONNECTED!"
		console.log("failed")
		errorMessage.innerHTML = "Failed to connect!"
	}
	
}

async function saveAPIKey(){
	
	//Get data from Javascript form
	userKey = document.getElementById("apikey")
	let userKeyValue = userKey.value;
	
	//Package Javascript data in a JSON format
	const info = {
		"key": userKeyValue
	};
	
	//Send the data to Flask via a POST
	const data = await fetchUrlData("http://127.0.0.1:5000/createAPIKey", {
		method: 'POST',
		headers: { 'Content-Type' : 'application/json' },
		body: JSON.stringify(info)
	});
	
	//Receive data from Flask
	if(data["keyUploaded"]){
		window.location.replace("main.html")
	}
}

async function transcribe()
{
	// get audio from file input
	audio = document.getElementById("audioFile").files[0].name;
	
	// Package audio in json
	const info = {
		"file": audio
	}
	
	//Send to Flask
	const transcription = await fetchUrlData("http://127.0.0.1:5000/transcribeAudio", {
		method: 'POST',
		headers: { 'Content-Type' : 'application/json' },
		body: JSON.stringify(info)
	});
	
	console.log(transcription)
	
	console.log(audio)
}
