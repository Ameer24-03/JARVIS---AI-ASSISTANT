import pyttsx3
import speech_recognition as sr
import eel
import time


# Text to Speech
def speak(text):
    text = str(text)

    engine = pyttsx3.init('sapi5')

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.setProperty('rate', 174)

    eel.DisplayMessage(text)

    engine.say(text)
    eel.receiverText(text)

    engine.runAndWait()


# Voice Recognition
def takecommand():

    r = sr.Recognizer()

    # Improve accuracy
    r.energy_threshold = 300
    r.pause_threshold = 1.2
    r.dynamic_energy_threshold = True

    with sr.Microphone() as source:

        print("Listening...")
        eel.DisplayMessage("Listening...")

        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=8)
        except:
            return ""

    try:

        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")

        query = r.recognize_google(audio, language='en-IN')

        print(f"User said: {query}")

        eel.DisplayMessage(query)

        time.sleep(1)

        return query.lower()

    except sr.UnknownValueError:
        speak("Sorry I did not understand, please say again")
        return ""

    except sr.RequestError:
        speak("Speech service is unavailable")
        return ""


# Main Command Handler
@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)

    else:
        query = message
        eel.senderText(query)

    try:

        # OPEN WEBSITE / APPS
        if "open" in query:

            from engine.features import openCommand
            openCommand(query)


        # PLAY YOUTUBE SONG
        elif "youtube" in query or "play" in query:

            from engine.features import PlayYoutube
            PlayYoutube(query)


        # CALL / MESSAGE COMMANDS
        elif "send message" in query or "call" in query or "video call" in query:

            from engine.features import findContact, whatsApp, makeCall, sendMessage

            contact_no, name = findContact(query)

            if contact_no != 0:

                # DIRECT CALL COMMAND
                if "call" in query and "message" not in query:

                    speak("Calling " + name)
                    makeCall(name, contact_no)

                # MESSAGE COMMAND
                elif "send message" in query:

                    speak("Which mode do you want, WhatsApp or mobile")

                    preference = takecommand()

                    if "mobile" in preference:

                        speak("What message should I send")
                        message = takecommand()

                        sendMessage(message, contact_no, name)

                    elif "whatsapp" in preference:

                        speak("What message should I send")
                        message = takecommand()

                        whatsApp(contact_no, message, "message", name)

                    else:
                        speak("Please say WhatsApp or mobile")

                # VIDEO CALL
                elif "video call" in query:

                    whatsApp(contact_no, "", "video call", name)


        # AI CHATBOT
        else:

            from engine.features import geminai
            geminai(query)

    except Exception as e:

        print("Error:", e)

    eel.ShowHood()