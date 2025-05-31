from datetime import datetime
from random import sample
from subprocess import call
from time import time
from unittest import result
import pyttsx3
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

# text-to-Speech Setup
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

# # Simple chatbot logic
# def simple_chatbot(user_input):
#     user_input = user_input.lower()

#     for question, answer in qa_pairs.items():
#         if question in user_input:
#             return answer

#         if "exit" in user_input or "quit" in user_input or "bye" in user_input:
#             return "GoodBye!"

#         return "Sorry, I didn't understand that."

# Load vosk model
model = Model("models")
recognizer = KaldiRecognizer(model, 16000)

# Create audio queue
q = queue.Queue()

# Audio callback
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Start listening from mic
# with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
#     print("Listening.... (say 'exit' to quit)")
#     buffer_text = ""

#     while True:
#         data = q.get()

#         if recognizer.AcceptWaveform(data):
#             result = json.loads(recognizer.Result())
#             text = result.get("text", "").strip()
            
#             if text:
#                 print("You said:", text)
#                 reply = simple_chatbot(text)
#                 speak(reply)

#                 if "goodbye" in reply.lower():
#                     break

#         else:
#             continue

# qa_pairs = {
#     "hello": "Hi there!",
#     "your name": "I'm your offline assistant.",
#     "how are you": "I'm doing great!",
#     "who made you": "I was made by my Mr M",
#     "capital of india": "The capital of India is New Delhi.",
#     "capital of usa": "The capital of USA is Washington, D.C.",
#     "what is python": "Python is a programming language.",
#     "what is ai": "AI stands for Artificial Intelligence."
    
# }




#GPT4all model

#Load the model

from gpt4all import GPT4All

model = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin",model_path="./models")

def smart_chatbot(user_input):
    with model.chat_session():
        response = model.generate(user_input, temp=0.3)
        return response

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
    print("Listening.... (say 'exit' to quit)")
    buffer_text = ""

    while True:
        data = q.get()

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip()
            
            if text:
                print("You said:", text)

                # Exit Condition
                if "exit" in text.lower() or "quit" in text.lower():
                    speak("GoodBye!")
                    break
                
                reply = smart_chatbot(text)
                print("Bot:", reply)
                speak(reply)
                
        else:
            continue

        time.sleep(0.1)