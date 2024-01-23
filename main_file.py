import humingbird
import streamlit as st
import time
import pyttsx3
import speech_recognition as sr
import datetime
import sys
import os
import random
import string
from gtts import gTTS
from playsound import playsound
from audiorecorder import audiorecorder
import wave

engine = pyttsx3.init('dummy')
voices=engine.getProperty('voices')

# voices[0] and voices[1] are the available voice in pyttsx3
#engine.setProperty('voice',voices[1].id)
def speak(audio):
    myobj = gTTS(text=audio, lang='en', slow=False)
    myobj.save("speak.mp3")
    playsound("speak.mp3",False)

    
def takeCommand():
    ## take microphhone inputand   return string output
    r=sr.Recognizer()
    with sr.Microphone() as source :
        print('listening...')
        audio=r.listen(source, phrase_time_limit=5)
        print('stoped listening.')
    try:
        print('recognizing...')
        
        # goole recognize is used to convert audio in to string
        query=r.recognize_google(audio)
        print('you said: ',query)
    
    except:
        print('say it again please.')
        return 'None'
    
    return query




intents = {
  "greeting": ["Hi! Welcome to DPS Noida Sector 30, school.", "Welcome! You can ask me about DPS noida Sector 30 school", "Hello! What you want to know about DPS Noida Sector 30 school?"],
  "information about school": ["DPS Noida is a co-educational day and boarding private school, educating pupils from Nursery to 12th grades, located in Sector-30 Noida.It is Founded in 1982. "],
  "goodbye": ["Goodbye!", "Nice chatting!", "Bye! Have a great day"],
  "Thank you": ["My pleasure", "Thank you! Have a great day"],
  "principal": ["The principal of DPS noida is Shri S. L. Dhawan Sir"],
  "Facilities": ["Our school have world class facilities like smart classrooms, Library, Computer Labs and Science Labs"],
  "Global": ["DPS Noida has an unprecedented five student exchange programs, running concurrently, with schools of Germany, Denmark, Spain, Swedan, and Switzerland. The oldest program, the Indo German student exchange program, has entered its fourteenth year and has the strong support of Max Mueller Bhawan, Goethe Institute, India."],
  "international program": ["DPS Noida have 5 student exchange program with schools of Germany, Denmark, Spain, Swedan, and Switzerland."],
  "vice principal":["Mrs. Manisha Sondhi is the vice principal of our school"],
  "Admission":["The Process of Admission is as follows: 1). You have to fill an online application form. 2). you child has to undergo an entrance test. 3). On account of seats being very limited, the admission process focuses on getting to know an applicant very well through interaction & academic assessment. "], 
  "Fees":["To get your child enrolled in DPS Noida you will have to pay fees between INR 1,50,000- 1,85,000, it can vary according to the class you are getting your child enrolled in."]
}


def detect_and_respond(query):
    prediction = humingbird.Text.predict(
    text=query,
    labels=["greeting", "information about school", "goodbye", "Thank you", "principal", "Facilities", "international program", "vice principal", "Admission","Fees"]
    )
    highest_score = 0
    highest_score_class = ""
    for i in prediction:
        if i["score"] > highest_score:
            highest_score = i["score"]
            highest_score_class = i["className"]

    return random.choice(intents[highest_score_class])

def takeCommandNew():
    r=sr.Recognizer()

# Read the audio data from the WAV file.
    with wave.open('audio.wav', 'rb') as wf:
        nframes = wf.getnframes()
        audio = wf.readframes(nframes)
    try:
        print('recognizing...')
        
        # goole recognize is used to convert audio in to string
        query=r.recognize_google(audio)
        print('you said: ',query)
    except:
        print('say it again please.')
        return 'None'
    return query

# Set the page title
st.title("SCHOOL AI ASSISTANT ")

# # Display the response
# #st.write(response)

# audio = audiorecorder("Click to record", "Click to stop recording")

# if len(audio) > 0:
#     # To play audio in frontend:
#     st.audio(audio.export().read())  

#     # To save audio to a file, use pydub export method:
#     audio.export("audio.wav", format="wav")

#     # To get audio properties, use pydub AudioSegment properties:
#     st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")
#     st.write('Processing the speech..!')
#     quest = takeCommandNew()
#     response = detect_and_respond(quest)

#     t = st.empty()
#     for i in range(len(response) + 1):
#         t.markdown("## %s..." % response[0:i])
#         time.sleep(0.1)

if st.button('Text'):
    # Get the user's question
    question = st.text_input("Enter your question:")
    #print(question)
    # Generate the response
    response = detect_and_respond(question)

    t = st.empty()
    speak(response)
    for i in range(len(response) + 1):
        t.markdown("## %s..." % response[0:i])
        time.sleep(0.09)


def newfunc():
    # Create a recognizer instance
    recognizer = sr.Recognizer()
    source=sr.Microphone()
    # Start recording audio
    with sr.Microphone() as source :
        print('listening...')
        #udio=r.listen(source, phrase_time_limit=5)
        print('stoped listening.')
        with st.spinner('Listening...'):
            audio = recognizer.listen(source,phrase_time_limit=5)

    # Try to recognize speech in the audio
    try:
        text = recognizer.recognize_google(audio)
        st.success(f'You said: {text}')
        # Generate the response
        response = detect_and_respond(text)
        speak(response)
        t = st.empty()
        for i in range(len(response) + 1):
            t.markdown("## %s..." % response[0:i])
            time.sleep(0.09)
    except sr.UnknownValueError:
        st.error('Could not understand your speech')

if st.button('Mic'):
    newfunc()