from playsound import playsound
import eel

# Play assistant sound function


@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.wav"
    playsound(music_dir)
