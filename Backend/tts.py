import os
import edge_tts
from dotenv import dotenv_values
import asyncio
import pygame
import random
global responses
responses = [
    "The rest of the result has been printed to the chat screen, kindly check it out sir.",
    "The rest of the text is now on the chat screen, sir, please check it.",
    "You can see the rest of the text on the chat screen, sir.",
    "The remaining part of the text is now on the chat screen, sir.",
    "Sir, you'll find more text on the chat screen for you to see.",
    "The rest of the answer is now on the chat screen, sir.",
    "Sir, please look at the chat screen, the rest of the answer is there.",
    "You'll find the complete answer on the chat screen, sir.",
    "The next part of the text is on the chat screen, sir.",
    "Sir, please check the chat screen for more information.",
    "There's more text on the chat screen for you, sir.",
    "Sir, take a look at the chat screen for additional text.",
    "You'll find more to read on the chat screen, sir.",
    "Sir, check the chat screen for the rest of the text.",
    "The chat screen has the rest of the text, sir.",
    "There's more to see on the chat screen, sir, please look.",
    "Sir, the chat screen holds the continuation of the text.",
    "You'll find the complete answer on the chat screen, kindly check it out sir.",
    "Please review the chat screen for the rest of the text, sir.",
    "Sir, look at the chat screen for the complete answer."
]
env_vars = dotenv_values(".env")
voice = env_vars.get("AssistantVoice")

async def TextToAudioFile(text):
    file_path = r"Data\speech.mp3" # Define the path where the speech file will be saved

    if os.path.exists(file_path): # Check if the file already exists
        os.remove(file_path) # If it exists, remove it to avoid overwriting errors

# Create the communicate object to generate speech
    communicate = edge_tts.Communicate(text, voice=voice, pitch='-7Hz', rate='+5%')
    await communicate.save(r'Data\speech.mp3') # Save the generated speech as an MP3 file

def TTS(Text, func=lambda r=None: True):
    try:
        while True:
            asyncio.run(TextToAudioFile(Text))
            pygame.mixer.init()
            pygame.mixer.music.load(r'Data\speech.mp3')
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)
            return True
    except Exception as e:
        print(f"Error: {e}")

    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error: {e}")

def text_to_speech(Text, func=lambda r=None: True):
    Data = str(Text).split('.')

    if len(Data) > 4 and len(Text) > 300:
        TTS(" ".join(Text.split('.')[0:2]) + ". "+ random.choice(responses), func)
    
    else:
        TTS(Text, func)