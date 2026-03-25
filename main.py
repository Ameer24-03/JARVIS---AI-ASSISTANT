import eel

from engine.features import *
from engine.command import *
from engine.auth import recoganize


# Initialize EEL with the UI folder
eel.init("www")


# Function called from JavaScript when the page loads
@eel.expose
def init():

    speak("Ready for Face Authentication")

    # Start face recognition
    flag = recoganize.AuthenticateFace()

    if flag == 1:

        # Hide loading screen
        eel.hideLoader()

        # Hide face authentication animation
        eel.hideFaceAuth()

        speak("Face Authentication Successful")

        # Hide face success message
        eel.hideFaceAuthSuccess()

        speak("Hello Sir, Welcome. How can I help you?")

        # Show assistant interface (Mic + Siri animation)
        eel.hideStart()

        # Play assistant sound
        playAssistantSound()

    else:
        speak("Face Authentication Failed")


# Start Jarvis UI
def start():
    eel.start(
        'index.html',
        mode='chrome',   # Opens Jarvis like a desktop app
        size=(1200, 800),
        port=8000
    )