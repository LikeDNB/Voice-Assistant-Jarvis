import os
import re
from playsound import playsound
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit

# Play assistant sound function


@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.wav"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    if query != "":
        speak("Opening"+query)
        os.system("start "+query+".exe")
    else:
        speak("not found")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on Youtube")
    kit.playonyt(search_term)


def extract_yt_term(command):
    # Define Regual expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match on the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name,
    # otherwise, return None
    return match.group(1) if match else None
