import speech_recognition as sr
import pyaudio
import pyttsx3
import time
import pvporcupine
import struct

USER = "okay"


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    print("J.A.R.V.I.S.: " + text + " \n")
    engine.say(text)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...", end="")
        speak("listening")
        audio = r.listen(source)
        query = ''
        try:
            print("Recognizing...", end="")
            query = r.recognize_google(audio, language='en-US')
            print(f"User said: {query}")

        except Exception as e:
            print("Exception: " + str(e))

    return query.lower()


def conversation_Flow():
    while True:
        user_said = take_command()
        if "hello" in user_said:
            speak("hello")
        if "bye" in user_said:
            speak("goodbye")
        if "how are you" in user_said:
            speak("Doing well")
        if "stop" in user_said:
            speak("Stopping sir")
            break
        if "exit" in user_said:
            speak("ending sir")
            break
        if "open my email" in user_said:
            speak("This is where i would run a program")

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
