import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "fb7636ad4a3b4d869f07022b8f8afd7a"


def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(
    api_key="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"
    )
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Rudra. Skilled to perform tasks like alexa and google Cloud"},
        {
            "role": "user",
            "content": command
        }
    ]
    )

    return completion.choices[0].message

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            #parse the json response
            data = r.json()

            #Extract the articles
            articles = data.get('articles',[])

            #print the headlines
            for article in articles:
                speak(article['title'])
                print(article['title'])

    else:
        #Let Openai handle it
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Rudra...")
    while True:
        #Listen for the wake word "Rudra"
        #obtain audio from microphone
        r = sr.Recognizer()
        

        #recognize speech 
        try:
            with sr.Microphone() as source:
                print("Listening you....")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "rudra"):
                speak("Yes")
                #Listen for command
                with sr.Microphone() as source:
                    print("Rudra Active....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))