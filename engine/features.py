import os
import re
from playsound import playsound
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import webbrowser
import sqlite3

con = sqlite3.connect("assistant.db")
cursor = con.cursor()

# Play assistant sound function


@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.wav"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()
    # old code before changes
    # if query != "":
    #     speak("Opening"+query)
    #     os.system("start "+query+".exe")
    # else:
    #     speak("not found")
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                """SELECT path FROM sys_command WHERE name IN (?)""",
                (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                    """SELECT url FROM web_command WHERE name IN (?)""",
                    (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system("start "+query)
                    except Exception as e1:
                        speak(f" Error {e1}: Not found")

        except Exception as e2:
            speak(f"Error {e2}: Something went wrong")


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
