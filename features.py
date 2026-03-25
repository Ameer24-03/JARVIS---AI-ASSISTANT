import json
import os
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine
import requests

from engine.helper import extract_yt_term, markdown_to_text, remove_words
from hugchat import hugchat
import google.generativeai as genai


# DATABASE
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()


# CUSTOM CONTACTS
CUSTOM_CONTACTS = {
    "ameer": "6281294994",
    "amma": "8186888554",
    "venkat": "9398599246"
}


# Assistant sound
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)


# OPEN COMMAND
def openCommand(query):

    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.strip().lower()

    websites = {
        "youtube": "https://www.youtube.com",
        "canva": "https://www.canva.com",
        "netflix": "https://www.netflix.com",
        "spotify": "https://open.spotify.com",
        "brave": "https://www.brave.com"
    }

    if query in websites:
        speak("Opening " + query)
        webbrowser.open(websites[query])
        return

    try:

        cursor.execute(
            'SELECT path FROM sys_command WHERE name IN (?)', (query,))
        results = cursor.fetchall()

        if len(results) != 0:
            speak("Opening " + query)
            os.startfile(results[0][0])

        else:

            cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (query,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                webbrowser.open(results[0][0])

            else:
                speak("Searching " + query)
                webbrowser.open("https://www.google.com/search?q=" + query)

    except:
        speak("Something went wrong")


# YOUTUBE PLAY
def PlayYoutube(query):

    search_term = extract_yt_term(query)

    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)


# SPOTIFY PLAY (AUTO PLAY FIRST TRACK)
def PlaySpotify(query):

    song = query.replace("play", "")
    song = song.replace("on spotify", "")
    song = song.strip()

    if song:

        speak("Playing " + song + " on Spotify")

        search_url = "https://api.spotify.com/v1/search"

        params = {
            "q": song,
            "type": "track",
            "limit": 1
        }

        try:

            # simple public search endpoint
            r = requests.get("https://open.spotify.com/search/" + song.replace(" ", "%20"))

            track_url = "https://open.spotify.com/search/" + song.replace(" ", "%20")

            webbrowser.open(track_url)

        except:

            webbrowser.open("https://open.spotify.com/search/" + song.replace(" ", "%20"))


# HOTWORD
def hotword():

    porcupine = None
    paud = None
    audio_stream = None

    try:

        porcupine = pvporcupine.create(keywords=["jarvis"])

        paud = pyaudio.PyAudio()

        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        while True:

            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from(
                "h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:

                print("hotword detected")

                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")

    except:

        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if paud is not None:
            paud.terminate()


# FIND CONTACT
def findContact(query):

    query = query.lower()

    for name in CUSTOM_CONTACTS:

        if name in query:

            number = CUSTOM_CONTACTS[name]

            return number, name

    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to',
                       'phone', 'call', 'send', 'message', 'whatsapp', 'video']

    query = remove_words(query, words_to_remove)

    try:

        query = query.strip().lower()

        cursor.execute(
            "SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ?",
            ('%' + query + '%',)
        )

        results = cursor.fetchall()

        mobile_number_str = str(results[0][0])

        return mobile_number_str, query

    except:

        speak("Contact not found")

        return 0, 0


# WHATSAPP MESSAGE
def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':

        speak("Sending message to " + name)

        message = message.replace(" ", "%20")

        url = f"https://wa.me/{mobile_no}?text={message}"

        webbrowser.open(url)

    elif flag == 'call':

        speak("Opening WhatsApp call with " + name)

        url = f"https://wa.me/{mobile_no}"

        webbrowser.open(url)

    else:

        speak("Opening WhatsApp video call with " + name)

        url = f"https://wa.me/{mobile_no}"

        webbrowser.open(url)


# CALL FUNCTION
def makeCall(name, mobileNo):

    speak("Calling " + name)

    url = f"https://wa.me/{mobileNo}"

    webbrowser.open(url)


# SEND MESSAGE
def sendMessage(message, mobileNo, name):

    speak("Sending message to " + name)

    message = message.replace(" ", "%20")

    url = f"https://wa.me/{mobileNo}?text={message}"

    webbrowser.open(url)


# CHATBOT
def chatBot(query):

    user_input = query.lower()

    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")

    id = chatbot.new_conversation()

    chatbot.change_conversation(id)

    response = chatbot.chat(user_input)

    speak(response)

    return response


# GEMINI AI
def geminai(query):

    try:

        query = query.replace(ASSISTANT_NAME, "")
        query = query.replace("search", "")

        genai.configure(api_key="AIzaSyCZDHFIAh3jOCAxqP7PUzMSbtWIkyGaFa0")

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(query)

        filter_text = markdown_to_text(response.text)

        speak(filter_text)

    except Exception as e:

        print("Error:", e)


# ASSISTANT NAME
@eel.expose
def assistantName():
    return ASSISTANT_NAME