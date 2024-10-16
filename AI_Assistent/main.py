import pywhatkit
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
import os
from googletrans import Translator
from gtts import gTTS
from playsound import playsound

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            talk('listening')
            listener.adjust_for_ambient_noise(source, duration=0.1)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            # if 'same' in command:
            #     command = command.replace('same', '')
            #     print(command)

    except sr.UnknownValueError:
        print("Sorry, I did not understand your command")
        pass
    return command


# def tranlate_voice(command, country_language_code):
#     translator = Translator()
#     # Translate the text
#     translated_text = translator.translate(command, dest=country_language_code).text
#     talk(translated_text)


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


def translate_to_bengali(text):
    translator = Translator()
    translate = translator.translate(text, dest='bn').text
    print(translate)
    tts = gTTS(text=translate, lang='bn')
    tts.save("output.mp3")
    playsound("output.mp3")


def run_same():
    command = take_command()
    print(command)
    if "okay" in command:
        command = command.replace("okay", '')
        print("How can i help you sir")
        talk("How can i help you sir")
        command = take_command()
        print(command)

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
            new_command = take_command()
            text = new_command
            translate_to_bengali(text)

    else:
        talk('Please say the name of your system again')


while True:
    run_same()
