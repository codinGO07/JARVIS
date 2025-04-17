from AppOpener import close, open as appopen # Import functic
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq 
import os 
from webbrowser import open as webopen
from pywhatkit import search, playonyt
import webbrowser
import subprocess
import requests
import keyboard
import asyncio

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "ZØLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta"
"IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e",
"LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

client = Groq(api_key=GroqAPIKey)
messages = []
SystemChatBot = [{'role': 'system', 'content': f"Hello, I am {os.environ['Username']}. You are a content writer. You have to write articles, essays, codes, songs, notes and other content."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])
    def ContentWriterAI(prompt):
        messages.append({'role': 'user', 'content': prompt})
        completion = client.chat.completions.create(
            model = "mistral-saba-24b",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        Answer = ""
        for chunk in completion:
            if chunk. choices[0].delta.content: # Check for content in the current chunk.
                Answer += chunk. choices[0].delta.content
        Answer = Answer. replace("</s>", "")
        messages.append({'role': 'assistant', 'content': Answer})
        return Answer
    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding='utf_8') as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
    return True

def YoutubeSearch(Topic):
    Url4Search = f'https://www.youtube.com/results?search_query={Topic}'
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname':'UWckNb'})
            return [link['href'] for link in links]
        def search_google(query):
            url = f'https://www.google.com/search?q={query}'
            headers = {'User-Agent': user_agent}
            response = sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                print('Failed to fetch the search results')
            return None
        html = search_google(app)
        if html:
            link = extract_links(html)[0]
            webopen(link)
        return True
def closeApp(app):
    if 'Chrome' in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False
def System(Command):
    def mute():
        keyboard.press_and_release('volume mute')

    def unmute():
        keyboard.press_and_release('volume mute')

    def volumeup():
        keyboard.press_and_release('volume up')
    def volumedown():
        keyboard.press_and_release('volume down')

    if Command=='mute':
        mute()
    elif Command=='unmute': 
        unmute()
    elif Command=='volume up':
        volumeup()
    elif Command=='volume down':
        volumedown()
    return True

async def TranslateAndExecute(commands: list[str]):

    funcs = [] # List to store asynchronous tasks.

    for command in commands:    
        if command.startswith("open "): # Handle "open" commands.
            if "open it" in command: # Ignore "open it" commands.
                pass
            if "open file" == command: # Ignore "open file" commands.
                pass
            else:
                fun = asyncio. to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "): # Placeholder for general commands.
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio. to_thread(closeApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("paly "):
            fun = asyncio. to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio. to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio. to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio. to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio. to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"Command not found: {command}")
    results = await asyncio. gather(*funcs)
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass

    return True