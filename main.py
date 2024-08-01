import os
import eel
from engine.features import playAssistantSound
from engine.features import openCommand
from engine.features import PlayYoutube
from engine.features import hotword
from engine.command import speak
from engine.command import takecommand
from engine.command import allCommands
from engine.features import findContact
from engine.features import whatsApp


unused_imports = False
if unused_imports is True:
    openCommand()
    PlayYoutube()
    hotword()
    speak()
    takecommand()
    allCommands()
    findContact()
    whatsApp()


def start():
    eel.init("www")
    playAssistantSound()
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)
