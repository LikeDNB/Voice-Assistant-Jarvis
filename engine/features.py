import os
import struct
import time
from playsound import playsound
import eel
import pyaudio
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import webbrowser
import sqlite3
from engine.helper import extract_yt_term
import pvporcupine


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


def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Pre trained keywords
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate,
                                 channels=1,
                                 format=pyaudio.paInt16,
                                 input=True,
                                 frames_per_buffer=porcupine.frame_length)

        # loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h"*porcupine.frame_length,
                                         keyword)

            # processing keyword comes from mic
            keyword_index = porcupine.process(keyword)

            # checking first keyword detected for not
            if keyword_index >= 0:
                print("hotword detected")

                # pressing shortcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except Exception as e:
        if porcupine is not None:
            porcupine.delete()
            print(e, "porcupine deleted")
        if audio_stream is not None:
            audio_stream.close()
            print(e, "audio_stream closed")
        if paud is not None:
            paud.terminate()
            print(e, "paud terminated")
