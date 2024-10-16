import pyaudio
import time
import pvporcupine
import struct
import pywhatkit
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
import os
from googletrans import Translator
import iso639

USER = "okay"


def talk(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    print(" " + text + " \n")
    engine.say(text)
    engine.runAndWait()


def play_on_youtube(command):
    sing = command.replace('play', '')
    sing_song = command.replace('song', '')
    new_play = sing + sing_song
    talk('playing...')
    pywhatkit.playonyt(new_play)


def search_on_google(command):
    search1 = command.replace('google', '')
    talk('searching...' + search1)
    pywhatkit.search(search1)


def search_on_wikipedia(command):
    item = command.replace('wikipedia', '')
    info = wikipedia.summary(item, 1)  # 1 for search only 1 line
    print(info)
    talk(info)


def tell_time(command):
    time = datetime.datetime.now().strftime('%I:%M %p')  # (I for 12 hour time formet) and (P for AM or PM)
    print(time)
    talk("It's " + time)


def tell_a_joke(command):
    a = pyjokes.get_joke()
    print(a)
    talk(a)


def power_compurte(command):
    print("What you want to do with your system. shutdown, restart, sleep")
    talk("What you want to do with your system. shutdown, restart, sleep")
    while True:
        command = take_command()
        if "restart" in command:  # for restart
            print("Are you sure you want to restart your system")
            talk("Are you sure you want to restart your system")
            while True:
                command = take_command()
                if "no" in command:
                    print("Thank you for use me, You can use me later.")
                    talk("Thank you for use me, You can use me later.")
                    break
                elif "yes" in command:
                    print("Restarting....")
                    talk("Restarting")
                    os.system("shutdown /r /t 40")
                    break
                talk("Say that again please")

        elif "shutdown" in command:  # for shutdown
            print("Are you sure you want to shutdown your system")
            talk("Are you sure you want to shutdown your system")
            while True:
                command = take_command()
                if "no" in command:
                    talk("Thank you for use me, You can use me later.")
                    break
                elif "yes" in command:
                    print("Shutting down")
                    talk("Shutting down")
                    os.system("shutdown /s /t 40")
                    break
                talk("Say that again please")
        talk("Say that again please")


def introduction(command):
    print("Hi, I am okay. A virtual assistant made by Ahamad safat.")
    talk("Hi, I am okay. A virtual assistant made by Ahamad safat.")


def all_search_function(command):
    print("What you want to do")
    talk("What you want to do")
    command_1 = take_command()
    if 'play' in command_1:
        play_on_youtube(command)

    elif 'google' in command_1:
        search_on_google(command)

    elif 'wikipedia' in command_1:
        search_on_wikipedia(command)
    else:
        print("Thank you")
        talk("Thank you")


def translate_to_bengali(text):
    print("Which language you want to translate")
    talk("Which language you want to translate")
    new_text = take_command()
    try:
        code = iso639.to_iso639_1(new_text)
    except KeyError:
        try:
            code = iso639.to_iso639_2(new_text)
        except KeyError:
            code = None
    print(code)
    translator = Translator()
    translate = translator.translate(text, dest=code).text
    print(translate)
    print("Do you want to do anything")
    talk("Do you want to do anything")
    command = take_command()
    if 'yes' in command:
        all_search_function(translate)
    elif 'no' in command:
        all_search_function(text)
    else:
        print("Please say again")
        talk("Please say again")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...", end="")
        talk("listening")
        audio = r.listen(source)
        query = ''
        try:
            print("Recognizing...", end="")
            query = r.recognize_google(audio, language='en-US')
            print(f"User said: {query}")

        except Exception as e:
            print("Exception: "+str(e))

    return query.lower()


def run_same():
    command = take_command()
    print(command)
    if "okay" in command:
        command = command.replace("okay", '')
        print("How can i help you sir")
        talk("How can i help you sir")
        command = take_command()
        print(command)
        while True:

            if 'play' in command:
                play_on_youtube(command)

            elif 'google' in command:
                search_on_google(command)

            elif 'wikipedia' in command:
                search_on_wikipedia(command)

            elif 'time' in command:
                tell_time(command)

            elif 'joke' in command:
                tell_a_joke(command)

            elif 'close computer' in command:
                power_compurte(command)

            elif "who are you" in command:
                introduction(command)

            elif "translate" in command:
                print("What you want to translate")
                talk("What you want to translate")
                new_command = take_command()
                text = new_command
                translate_to_bengali(text)

            elif "dot" in command:
                print("Stopping your system sir")
                talk("Stopping your system sir")
                break

    else:
        talk("I am unable to do it")


def conversation_Flow():
    while True:
        run_same()

        time.sleep(2)


def main():
    porcupine = None
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(keywords=["bumblebee", "computer"])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Hotword Detected...", end="")
                conversation_Flow()
                time.sleep(0.5)
                print("Awaiting your call " + USER)

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

main()