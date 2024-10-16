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
import pyautogui
import openai
from word2number import w2n
from AppOpener import open, close, mklist, give_appnames
from random import choices

USER = "sir"


def about():
    print("Hi, I am a virtual assistant made by Ahamad safat.")
    talk("Hi, I am a virtual assistant made by Ahamad safat.")

    print("I can play any thing on youtube and my keyword is play.")
    talk("I can play any thing on youtube and my keyword is play.")

    print("I can search on google and my keyword is google.")
    talk("I can search on google and my keyword is google.")

    print("I can search on wikipedia and my keyword is wikipedia.")
    talk("I can search on wikipedia and my keyword is wikipedia.")

    print("I can speak jokes and my keyword is joke.")
    talk("I can speak jokes and my keyword is joke.")

    print("I can open any software and my keyword is open.")
    talk("I can open any software and my keyword is open.")

    print("I can shutdown or restart your system and my keyword is close computer.")
    talk("I can shutdown or restart your system and my keyword is close computer.")

    print("I can tell you the time and my keyword is time")
    talk("I can tell you the time and my keyword is time.")

    print("I can translate your command and then search that on youtube, google, wikipedia and my keyword is translate")
    talk("I can translate your command and then search that on youtube, google, wikipedia and my keyword is translate.")

    print("I can use Open AI and the keyword is ai.")
    talk("I can use Open AI and the keyword is ai.")

    print("If you want to turn me off then my keyword is turn off")
    talk("If you want to turn me off then my keyword is turn off.")


def talk(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    print("")
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
    new_command = command.replace('wikipedia', '')
    talk("Type only the number of lines that you want the summary")
    command = take_command()
    stringNum = command.replace('lines', '')
    num_sentences = w2n.word_to_num(stringNum)
    intNum = int(num_sentences)
    talk(f"You want to take {intNum} lines")
    '''
    num = input("Type the number of lines \n")
    num_sentences = int(num)
    '''
    try:
        page = wikipedia.page(new_command)
        summary_sentences = page.summary.split('. ')[:intNum]
        print(summary_sentences)
        talk(summary_sentences)

    except wikipedia.exceptions.PageError:
        return "Page not found."

    except wikipedia.exceptions.DisambiguationError as e:
        return "Search query is ambiguous. Try one of the following: " + ", ".join(e.options)


def tell_time():
    set_time = datetime.datetime.now().strftime('%I:%M %p')  # (I for 12 hour time formet) and (P for AM or PM)
    print(set_time)
    talk("It's " + set_time)


def tell_a_joke():
    a = pyjokes.get_joke()
    print(a)
    talk(a)


def power_compurte():
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


openai.api_key = "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"
completion = openai.Completion()


def add_open_ai(command):
    new_command = command.replace('ai', '')
    prompt = f"hey: {new_command}\n"
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].text.strip()
    print(answer)
    talk(answer)


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
            print("Exception: " + str(e))
            talk("I can't recognize. Please say again.")

    return query.lower()


chatSTR = ""


def chat(command):
    openai.api_key = "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"
    command = command.replace("ai", "")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=command,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # todo: Wrap this inside of a try catch block

    talk(response["choices"][0]["text"])

    command += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

    # with open(f"Openai/prompt- (random.randint(1, 2343434356)}", "w") as f:

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def run_same():
    while True:
        print("At your service sir")
        talk("At your service sir")
        command = take_command()
        print(command)

        if "what is your name" in command or "what's your name" in command:
            talk("My name is BumbleBee")

        elif 'about' in command:
            about()

        elif 'play' in command:
            play_on_youtube(command)

        elif 'google' in command:
            search_on_google(command)

        elif 'wikipedia' in command:
            search_on_wikipedia(command)

        elif 'time' in command:
            tell_time()

        elif 'joke' in command:
            tell_a_joke()

        elif 'close computer' in command:
            power_compurte()

        elif 'translate' in command:
            print("What you want to translate")
            talk("What you want to translate")
            new_command = take_command()
            text = new_command
            translate_to_bengali(text)

        elif 'open' in command:
            command = command.replace("open", "")
            open(command.lower())

        elif 'close' in command:
            command = command.replace("close", "")
            close(command.lower())

        elif "ai" in command:
            chat(command)

        elif "turn off" in command:
            talk("Turning off your system sir")
            break

        # elif "reminder" in command:
        #     message = command.replace("reminder", "")
        #     re

        else:
            add_open_ai(command)

        time.sleep(2)


def main():
    print("listening...")
    talk("listening")
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
                print("Hotword Detected... " + "\n", end="")
                run_same()
                time.sleep(0.5)
                print("Awaiting your call " + USER)

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()


if __name__ == "__main__":
    main()
