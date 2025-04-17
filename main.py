from typing import Text
from Backend import Chatbot
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.stt import SpeechRecognition
from Backend.Chatbot import AnswerModifier, ChatBot
from Backend.tts import text_to_speech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
Default_message = f'''{Username} : Hello {Assistantname}, How are you ?
{Assistantname} : Welcome {Username}, I am doing well, How can I help you ?'''
subprocesses = []
Functions = ['open', 'close', 'play', 'sysyem', 'content', 'google search', 'youtube search']

def ReadChatLogJson():
    with open(r"Data\ChatLog.json", "r", encoding='utf-8') as f:
        chatlog_data = json.load(f)
    return chatlog_data

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    query = input("HEre :")
    Decision = FirstLayerDMM(query)

    print("")
    print("Decision : ", Decision)
    print("")

    G = any([i for i in Decision if i.startswith('general')])
    R = any([i for i in Decision if i.startswith('realtime')])

    MergedQuery = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith('general') or i.startswith('realtime')]
    )
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True
    for queries in Decision:
        if TaskExecution==False:
            if any(queries.startswith(func) for func in Functions):
                TaskExecution = True
    if ImageExecution==True:
        with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
            f.write(f'{ImageGenerationQuery},True')
        try:
            p1 = subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE, shell=False)
            subprocesses.append(p1)
        except Exception as e:
            print("Error : ", e)
    if G and R or R:
        Answer = RealtimeSearchEngine(AnswerModifier(MergedQuery))
        text_to_speech(Answer)
        return True
    else:
        for queries in Decision:
            if "general" in queries:
                query_final = queries.replace("general ", "")
                Answer = ChatBot(AnswerModifier(AnswerModifier(query_final)))
                text_to_speech(Answer)
                return True
            elif "realtime" in queries:
                query_final = queries.replace("realtime ", "")
                Answer = RealtimeSearchEngine(AnswerModifier(query_final))
                text_to_speech(Answer)
                return True
            
            elif "exit" in queries:
                query_final = "Bye"
                Answer = ChatBot(AnswerModifier(query_final))
                text_to_speech(Answer)
                os._exit(1)
# 

if __name__ == "__main__":
    while True:
        MainExecution()
            
            

    

