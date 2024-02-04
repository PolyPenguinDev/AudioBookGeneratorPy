import threading
import openai
from pydub import AudioSegment
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from gradio_client import Client

global CP
CP = []

model = "meta-llama/Llama-2-70b-chat-hf"

def speak_text(text):
    global CP
    global audio
    global star_time
    global currentlyplaying
    global sound
    currentlyplaying = CP
    CP = []

    sound = convert_text_to_audio(text)
    sound.export("welcome.mp3", format="mp3")
    pygame.init()
    sound = pygame.mixer.Sound("welcome.mp3")
    star_time = time.time()
    sound.play()
    while pygame.mixer.get_busy():
        pass

def convert_text_to_audio(text):
    global audio
    Au = AudioSegment.from_file(generate_audio(text))
    if len(audio) == 0:
        audio.append(Au)
    else:
        audio[0] += Au
    CP.append(len(Au) / 1000)
    return Au

def generate_audio(aud):
    global first
    out = client.predict(
        aud,
        "Charlie",
        fn_index=0
    )
    if not first:
        first = True
        print("✅ Finished Processing Prompt\n")
    return out

if __name__ == '__main__':
    client = Client("https://elevenlabs-tts.hf.space/", verbose=False)
    audio = []

    prompt = input("> ")

    speak_text(prompt)
