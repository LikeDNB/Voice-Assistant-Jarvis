import pyttsx3
import speech_recognition as sr
import eel


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

    engine.setProperty('voice', ru_voice_id)
    engine.setProperty('rate', 170)     # setting up new voice rate
    print(voices)
    engine.say(text)
    engine.runAndWait()


@eel.expose
def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("listening.....")
        eel.DisplayMessage("listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)

        audio = r.listen(source, timeout=None, phrase_time_limit=6)

    try:
        print("recognizing")
        eel.DisplayMessage("recognizing...")
        query = r.recognize_google(audio, language='ru-RU')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        speak(query)
        eel.ShowHood()

    except Exception as e:
        return f"{e}"

    return query.lower()
