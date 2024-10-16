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
import requests
import threading
from google.oauth2 import service_account
from googleapiclient.discovery import build
from twilio.rest import Client
import imaplib
import email
from word2number import w2n
from AppOpener import open, close, mklist, give_appnames
from random import choices

USER = "sir"

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# Function to speak a given text
def talk(text):
    try:
        print(text)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in talk function: {str(e)}")


# Function to describe the capabilities of BumbleBee
def about():
    capabilities = [
        "I can play any song or video on YouTube, just say 'play'.",
        "I can search on Google, just say 'google'.",
        "I can search on Wikipedia, just say 'wikipedia'.",
        "I can tell you the current time, just say 'time'.",
        "I can tell jokes, just say 'joke'.",
        "I can open and close applications, just say 'open' or 'close'.",
        "I can list all installed applications, just say 'list apps'.",
        "I can shutdown or restart your system, just say 'close computer'.",
        "I can translate text and search the result, just say 'translate'.",
        "I can interact with OpenAI for complex queries, just say 'ai'.",
        "I can set alarms, just say 'set alarm'.",
        "I can check your email, just say 'check email'.",
        "I can manage your to-do list, just say 'manage to-do list'.",
        "I can control smart devices, just say 'control smart home'.",
        "I can give you traffic updates, just say 'traffic'.",
        "I can send text messages, just say 'send message'.",
        "I can read out your calendar events, just say 'calendar'.",
        "I can turn off when you say 'turn off'."
    ]
    for capability in capabilities:
        try:
            talk(capability)
        except Exception as e:
            print(f"Error in about function: {str(e)}")


# Function to play media on YouTube
def play_on_youtube(command):
    try:
        search_query = command.replace('play', '')
        talk('Playing on YouTube...')
        pywhatkit.playonyt(search_query)
    except Exception as e:
        talk(f"Sorry, I couldn't play on YouTube. Error: {str(e)}")


# Function to search on Google
def search_on_google(command):
    try:
        search_query = command.replace('google', '')
        talk(f'Searching Google for {search_query}...')
        pywhatkit.search(search_query)
    except Exception as e:
        talk(f"Sorry, I couldn't search on Google. Error: {str(e)}")


# Function to search on Wikipedia
def search_on_wikipedia(command):
    try:
        query = command.replace('wikipedia', '')
        talk("How many lines of summary would you like?")
        lines_command = take_command()
        num_sentences = w2n.word_to_num(lines_command.replace('lines', ''))
        talk(f"Fetching {num_sentences} lines from Wikipedia...")

        try:
            page = wikipedia.page(query)
            summary = page.summary.split('. ')[:num_sentences]
            summary_text = '. '.join(summary)
            talk(summary_text)
        except wikipedia.exceptions.PageError:
            talk("Page not found.")
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"Your search query is ambiguous. Try one of the following: {', '.join(e.options)}")
    except Exception as e:
        talk(f"Sorry, I couldn't search on Wikipedia. Error: {str(e)}")


# Function to tell the current time
def tell_time():
    try:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {current_time}")
    except Exception as e:
        talk(f"Sorry, I couldn't get the time. Error: {str(e)}")


# Function to tell a joke
def tell_a_joke():
    try:
        joke = pyjokes.get_joke()
        talk(joke)
    except Exception as e:
        talk(f"Sorry, I couldn't tell a joke. Error: {str(e)}")


# Function to shutdown, restart, or sleep the computer
def power_computer():
    try:
        talk("What would you like to do? Shutdown, restart, or sleep?")
        while True:
            command = take_command()
            if "restart" in command:
                talk("Are you sure you want to restart?")
                confirmation = take_command()
                if "yes" in confirmation:
                    talk("Restarting the system...")
                    os.system("shutdown /r /t 10")
                    break
            elif "shutdown" in command:
                talk("Are you sure you want to shutdown?")
                confirmation = take_command()
                if "yes" in confirmation:
                    talk("Shutting down the system...")
                    os.system("shutdown /s /t 10")
                    break
            elif "sleep" in command:
                talk("Putting the system to sleep...")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                break
    except Exception as e:
        talk(f"Sorry, I couldn't complete the system command. Error: {str(e)}")


# Function to translate and then search the translated text
def translate_and_search(command):
    try:
        talk("Which language would you like to translate to?")
        language = take_command()
        try:
            language_code = iso639.to_iso639_1(language)
        except KeyError:
            talk("Language not recognized. Please try again.")
            return

        translator = Translator()
        translation = translator.translate(command, dest=language_code).text
        talk(f"Translation: {translation}")

        talk("What would you like to do with the translation?")
        action = take_command()

        if 'play' in action:
            play_on_youtube(translation)
        elif 'google' in action:
            search_on_google(translation)
        elif 'wikipedia' in action:
            search_on_wikipedia(translation)
    except Exception as e:
        talk(f"Sorry, I couldn't complete the translation. Error: {str(e)}")


# Function to interact with OpenAI for text completion
def interact_with_openai(command):
    try:
        prompt = command.replace('ai', '')
        talk("Connecting to OpenAI...")
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
        talk(answer)
    except Exception as e:
        talk(f"Sorry, I couldn't connect to OpenAI. Error: {str(e)}")


# Function to take voice input from the user
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        talk("Listening...")
        audio = None
        try:
            audio = recognizer.listen(source, timeout=10)
        except sr.WaitTimeoutError:
            talk("I didn't hear anything. Would you like me to turn off, or do you have another command?")
            return None

        try:
            command = recognizer.recognize_google(audio, language='en-US')
            return command.lower()
        except sr.UnknownValueError:
            talk("Sorry, I didn't catch that. Please try again.")
            return take_command()
        except sr.RequestError:
            talk("Network error. Please check your connection.")
            return None
        except Exception as e:
            talk(f"Sorry, I couldn't process your command. Error: {str(e)}")
            return None


# Function to open an application
def open_application(app_name):
    try:
        talk(f"Opening {app_name}...")
        open(app_name.lower())
    except Exception as e:
        talk(f"Sorry, I couldn't open {app_name}. Error: {str(e)}")


# Function to close an application
def close_application(app_name):
    try:
        talk(f"Closing {app_name}...")
        close(app_name.lower())
    except Exception as e:
        talk(f"Sorry, I couldn't close {app_name}. Error: {str(e)}")


# Function to list all available applications
def list_applications():
    try:
        app_list = mklist(give_appnames())
        talk("Here are the applications installed on your system:")
        for app in app_list:
            talk(app)
    except Exception as e:
        talk(f"Sorry, I couldn't list the applications. Error: {str(e)}")


# Function to open or close applications based on the command
def handle_application_command(command):
    try:
        if 'open' in command:
            app_name = command.replace("open", "").strip()
            open_application(app_name)
        elif 'close' in command:
            app_name = command.replace("close", "").strip()
            close_application(app_name)
        elif 'list apps' in command:
            list_applications()
        else:
            talk("Sorry, I couldn't understand the command. Please try again.")
    except Exception as e:
        talk(f"Sorry, there was an error processing your application command. Error: {str(e)}")


# Function to set an alarm
def set_alarm():
    try:
        talk("When would you like to set the alarm?")
        alarm_time = take_command().replace(".", "").strip()
        talk(f"Setting an alarm for {alarm_time}.")

        def alarm_ring():
            while True:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                if current_time == alarm_time:
                    talk("Wake up! It's time!")
                    break
                time.sleep(10)

        threading.Thread(target=alarm_ring).start()
    except Exception as e:
        talk(f"Sorry, I couldn't set the alarm. Error: {str(e)}")


# Function to read out calendar events
def get_calendar_events():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            'path_to_service_account.json', scopes=['https://www.googleapis.com/auth/calendar.readonly'])
        service = build('calendar', 'v3', credentials=credentials)

        talk("Fetching your calendar events.")
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            talk("No upcoming events found.")
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                talk(f"Upcoming event: {event['summary']} at {start}")
    except Exception as e:
        talk(f"Sorry, I couldn't fetch the calendar events. Error: {str(e)}")


# Function to send text messages
def send_text_message():
    try:
        talk("Who do you want to send a message to?")
        recipient = take_command().lower()
        talk("What is the message?")
        message_body = take_command()

        client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")
        message = client.messages.create(
            body=message_body,
            from_='+1234567890',
            to='+0987654321'
        )
        talk(f"Message sent to {recipient}.")
    except Exception as e:
        talk(f"Sorry, I couldn't send the message. Error: {str(e)}")


# Function to create and manage to-do lists
todo_list = []


def manage_todo_list():
    try:
        talk("Would you like to add, view, or remove tasks from your to-do list?")
        action = take_command()

        if "add" in action:
            talk("What task would you like to add?")
            task = take_command()
            todo_list.append(task)
            talk(f"Task '{task}' added to your to-do list.")

        elif "view" in action:
            if todo_list:
                talk("Here are your to-do list tasks:")
                for i, task in enumerate(todo_list, start=1):
                    talk(f"Task {i}: {task}")
            else:
                talk("Your to-do list is empty.")

        elif "remove" in action:
            if todo_list:
                talk("Which task number would you like to remove?")
                task_number = int(take_command()) - 1
                if 0 <= task_number < len(todo_list):
                    removed_task = todo_list.pop(task_number)
                    talk(f"Task '{removed_task}' removed from your to-do list.")
                else:
                    talk("Invalid task number.")
            else:
                talk("Your to-do list is empty.")
    except Exception as e:
        talk(f"Sorry, I couldn't manage the to-do list. Error: {str(e)}")


# Function to get traffic information
def get_traffic_info():
    try:
        talk("Please tell me your current location.")
        current_location = take_command()
        talk("Where are you heading?")
        destination = take_command()

        api_key = "YOUR_GOOGLE_MAPS_API_KEY"
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={current_location}&destination={destination}&key={api_key}"

        response = requests.get(url)
        data = response.json()

        if data["status"] == "OK":
            routes = data["routes"][0]
            legs = routes["legs"][0]
            duration = legs["duration"]["text"]
            distance = legs["distance"]["text"]

            talk(f"It will take {duration} to reach {destination}, covering a distance of {distance}.")
        else:
            talk("Sorry, I couldn't get the traffic information.")
    except Exception as e:
        talk(f"Sorry, I couldn't get the traffic information. Error: {str(e)}")


# Function to set and manage reminders
reminders = []


def manage_reminders():
    try:
        talk("Would you like to add, view, or remove reminders?")
        action = take_command()

        if "add" in action:
            talk("What is the reminder?")
            reminder = take_command()
            reminders.append(reminder)
            talk(f"Reminder '{reminder}' added.")

        elif "view" in action:
            if reminders:
                talk("Here are your reminders:")
                for i, reminder in enumerate(reminders, start=1):
                    talk(f"Reminder {i}: {reminder}")
            else:
                talk("You have no reminders.")

        elif "remove" in action:
            if reminders:
                talk("Which reminder number would you like to remove?")
                reminder_number = int(take_command()) - 1
                if 0 <= reminder_number < len(reminders):
                    removed_reminder = reminders.pop(reminder_number)
                    talk(f"Reminder '{removed_reminder}' removed.")
                else:
                    talk("Invalid reminder number.")
            else:
                talk("You have no reminders.")
    except Exception as e:
        talk(f"Sorry, I couldn't manage reminders. Error: {str(e)}")


# Function to check email
def check_email():
    try:
        talk("Checking your email...")
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('your_email@gmail.com', 'your_password')
        mail.select('inbox')

        status, data = mail.search(None, '(UNSEEN)')
        mail_ids = data[0].split()

        if mail_ids:
            for num in mail_ids[:5]:
                status, msg_data = mail.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        talk(f"From: {msg['from']}")
                        talk(f"Subject: {msg['subject']}")
                        talk(f"Received on: {msg['date']}")
        else:
            talk("You have no new unread emails.")
        mail.logout()
    except Exception as e:
        talk(f"Sorry, I couldn't check your email. Error: {str(e)}")


# Function to control smart home devices
def control_thermostat(command):
    try:
        talk("What temperature would you like to set?")
        temperature = int(take_command())

        # Replace this with your actual smart home thermostat control logic
        talk(f"Setting thermostat to {temperature} degrees.")
    except Exception as e:
        talk(f"Sorry, I couldn't control the thermostat. Error: {str(e)}")


# Function to provide a daily briefing
def daily_briefing():
    try:
        talk("Good morning! Here's your daily briefing.")
        get_weather_report()
        get_calendar_events()
        get_news()
        manage_reminders()
    except Exception as e:
        talk(f"Sorry, I couldn't complete the daily briefing. Error: {str(e)}")


# Function to get fitness update
def get_fitness_update():
    try:
        talk("You have completed 6,500 steps today. Keep it up!")
        talk("You burned 500 calories today.")
    except Exception as e:
        talk(f"Sorry, I couldn't get your fitness update. Error: {str(e)}")


# Function to run the virtual assistant
def run_bumblebee():
    while True:
        try:
            talk("At your service, sir.")
            command = take_command()

            if command:
                if "what is your name" in command or "what's your name" in command:
                    talk("My name is BumbleBee.")
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
                    power_computer()
                elif 'translate' in command:
                    translate_and_search(command)
                elif 'open' in command or 'close' in command or 'list apps' in command:
                    handle_application_command(command)
                elif "ai" in command:
                    interact_with_openai(command)
                elif "wifi" in command:
                    scan_wifi()
                elif "bluetooth" in command:
                    scan_bluetooth()
                elif "set alarm" in command:
                    set_alarm()
                elif "calendar" in command:
                    get_calendar_events()
                elif "send message" in command:
                    send_text_message()
                elif "manage to-do list" in command:
                    manage_todo_list()
                elif "traffic" in command:
                    get_traffic_info()
                elif "reminders" in command:
                    manage_reminders()
                elif "check email" in command:
                    check_email()
                elif "control smart home" in command:
                    control_thermostat(command)
                elif "daily briefing" in command:
                    daily_briefing()
                elif "fitness update" in command:
                    get_fitness_update()
                elif "turn off" in command:
                    talk("Turning off BumbleBee. Goodbye!")
                    break
                else:
                    interact_with_openai(command)
            else:
                talk("Would you like to give another command or should I turn off?")
                command = take_command()
                if command and "turn off" in command:
                    talk("Turning off BumbleBee. Goodbye!")
                    break
        except Exception as e:
            talk(f"Sorry, an unexpected error occurred. Error: {str(e)}")
        time.sleep(2)


# Main function to initialize the hotword detection and run the assistant
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
            try:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    talk("Hotword detected, activating BumbleBee...")
                    run_bumblebee()
                    time.sleep(0.5)
            except Exception as e:
                talk(f"Sorry, an error occurred while processing audio. Error: {str(e)}")

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        talk(f"An error occurred in the main function. Error: {str(e)}")
