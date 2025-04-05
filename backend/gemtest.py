from google import genai

#client = genai.Client(api_key="AIzaSyD5mTUqDs4IVVicop8B0aaRPUKmb6Veq-U")
client = genai.Client(api_key="AIzaSyD5mTUqDs4IVVicop8B0aaRPUKmb6Veq-U")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a LOT of words"
)
print(response.text)
