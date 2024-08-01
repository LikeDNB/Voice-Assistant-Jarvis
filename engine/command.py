import pyttsx3
import speech_recognition as sr
import eel
import time


# Print all available voices
# import pyttsx3
# engine = pyttsx3.init()

# voices = engine.getProperty('voices')
# for voice in voices:
#     print("Voice:")
#     print(" - ID: %s" % voice.id)
#     print(" - Name: %s" % voice.name)
#     print(" - Languages: %s" % voice.languages)
#     print(" - Gender: %s" % voice.gender)
#     print(" - Age: %s" % voice.age)

en_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\\
Tokens\\TTS_MS_EN-US_ZIRA_11.0"
ru_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\\
Tokens\\TTS_MS_RU-RU_IRINA_11.0"


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)     # setting up new voice rate
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("listening.....")
        eel.DisplayMessage("listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.1)

        audio = r.listen(source, 10, 6)

    try:
        print("recognizing")
        eel.DisplayMessage("recognizing...")
        query = r.recognize_google(audio, language='en-EN')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        eel.ShowHood()

    except Exception as e:
        return f"{e}"

    return query.lower()


@eel.expose
def allCommands():

    try:
        query = takecommand()
        print(query)

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif ["send message" in query or
              "phone call" in query or
              "video call" in query]:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if (contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()

                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'

                whatsApp(contact_no, query, flag, name)
        else:
            print("not run")
    except Exception as e:
        print("error", e)

    eel.ShowHood()
