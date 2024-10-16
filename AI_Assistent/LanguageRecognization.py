# import langid
#
# texts = [
#     "This is a sample text.",
#     "Ceci est un texte d'exemple.",
#     "Dies ist ein Beispieltext.",
#     "これはサンプルテキストです。",
#     "Este es un texto de ejemplo.",
#     "আপনি কেমন আছেন",
#     "आप कैसे हैं"
# ]
#
# for text in texts:
#     language, confidence = langid.classify(text)
#     print(f"Text: {text}")
#     print(f"Language : {language}")
#     print(f"Detected language: {language} with confidence {confidence}\n")


# mp4 recognization

import moviepy.editor as mp
from pydub import AudioSegment
import speech_recognition as sr
import langid
import os


def extract_audio_from_video(video_file, audio_file):
    video = mp.VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)


def convert_audio_to_wav(audio_file, wav_file):
    audio = AudioSegment.from_file(audio_file)
    audio.export(wav_file, format="wav")


def recognize_speech_from_audio(wav_file):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(wav_file)
    with audio_file as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"


def classify_language(text):
    language, confidence = langid.classify(text)
    return language, confidence


def main(video_file):
    audio_file = "extracted_audio.mp3"
    wav_file = "extracted_audio.wav"

    # Step 1: Extract audio from video
    extract_audio_from_video(video_file, audio_file)

    # Step 2: Convert audio to wav format
    convert_audio_to_wav(audio_file, wav_file)

    # Step 3: Recognize speech from audio
    text = recognize_speech_from_audio(wav_file)
    print(f"Recognized Text: {text}")

    # Step 4: Classify language of the recognized text
    language, confidence = classify_language(text)
    print(f"Detected Language: {language} with confidence {confidence}")

    # Clean up
    os.remove(audio_file)
    os.remove(wav_file)


# Example usage
video_file = "try.mpg"
main(video_file)


#
# import moviepy.editor as mp
# import speech_recognition as sr
# import langid
# import os
#
#
# def convert_video_audio_to_wav(video_file, wav_file):
#     video = mp.VideoFileClip(video_file)
#     audio = video.audio
#     audio.write_audiofile(wav_file, codec='pcm_s16le', ffmpeg_params=['-ac', '1'])
#
#
# def recognize_bangla_speech_from_audio(wav_file):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(wav_file) as source:
#         audio = recognizer.record(source)
#     try:
#         text = recognizer.recognize_google(audio, language='bn-BD')  # Specify Bengali (Bangla) language
#         return text
#     except sr.UnknownValueError:
#         return "Speech recognition could not understand audio"
#     except sr.RequestError as e:
#         return f"Could not request results from Google Speech Recognition service; {e}"
#
#
# def main(video_file):
#     wav_file = "extracted_audio.wav"
#
#     # Step 1: Convert video audio to WAV format
#     convert_video_audio_to_wav(video_file, wav_file)
#
#     # Step 2: Recognize Bengali speech from audio
#     text = recognize_bangla_speech_from_audio(wav_file)
#     print(f"Recognized Text in Bengali: {text}")
#
#     # Clean up
#     os.remove(wav_file)
#
#
# # Example usage
# video_file = "1.mp4"
# main(video_file)




