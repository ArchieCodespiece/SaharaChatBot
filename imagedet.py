from ultralytics import YOLO
from langchain_groq import ChatGroq
import os

# API key and model initialization
kk = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=kk, model_name="gemma2-9b-it", temperature=0.3)
model = YOLO('best.pt')

# Function for image recognition
def recognition(image_upload):
    results = model(image_upload)
    detections = results[0].to_json()  # Structured output
    prompt = f"""
The YOLO model detected the following objects in this medical image: {detections}. 

1. Predict the probability percentage of any tumor detected.  
2. State the tumor type detected, if any.  
3. Provide a short and clear definition of the tumor detected.  
4. Do not include any disclaimers or cautious language. Be clear, confident, and concise.
"""
    response = llm.invoke(prompt)
    return response.content

# Provide the image path



