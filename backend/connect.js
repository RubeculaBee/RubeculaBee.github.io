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
			window.location.replace("backend/upload.html");
			
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
		window.location.replace("upload.html")
	}
}

async function askQuestion(){
	//userInstructions = document.getElementById("instructions").value;
	
	const info = {
		"instruction": "MAKE THIS A GET SOON!!!"
	};
	
	const data = await fetchUrlData("http://127.0.0.1:5000/question", {
		method: 'POST',
		headers: { 'Content-Type' : 'application/json' },
		body: JSON.stringify(info)
	});
	
	//Trim the ends of the output
	//summary = data["answer"].substring(7, data["answer"].length-3);
	//turn the output string into a json object
	//summary = JSON.parse(summary);
	
	summary = JSON.parse(data["answer"]);
	
	console.log(summary);
	
	//After this point we need to actually put the JSON onto the gemini page
	document.getElementById("topic").innerHTML = summary.topic;
	
	keyPointList = document.getElementById("kpoints");
	exampleProbList = document.getElementById("exampleProb");
	
	//Populate our Key Points List
	for( let i = 0; i < summary.keyPoints.length; i++){
		point = document.createElement('li');
		point.innerHTML = summary.keyPoints[i];
		keyPointList.appendChild(point);
	}
	
	//Populate our Example Problem List
	for( let i = 0; i < summary.exampleProblem.length; i++){
		step = document.createElement('li');
		step.innerHTML = summary.exampleProblem[i];
		exampleProbList.appendChild(step);
	}
	
	document.getElementById("notes").style.display = "block";
	document.getElementById("loadingArea").style.display = "none";
	
}	

function makeButton()
{
	continueButton = document.createElement('button');
	continueButton.innerHTML = "Continue"
	continueButton.onclick = function()
	{
		window.location.replace("gemini.html")
	}
	
	document.body.appendChild(continueButton);
}
