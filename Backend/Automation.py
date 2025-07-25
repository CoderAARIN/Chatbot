from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os


env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")


classes = ["zCubwaf", "hgKElc", "LTKOO", "Z0LcW", "gsrt vk_bk FzWSB YwnPhnf", "pclquee", "tw-Data-text-samll tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswer-webanswer_table__webanswer-table", "dDoNo ikb48b gsrt", "sXLaOe",
           "LWkfKe", "VQF4g", "kno-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) chrome/100.0.4896'


client = Groq(api_key=GroqAPIKey)

proffessional_responses = [
    "Your satisifaction is my top priority; fell free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional question or support you may-need don't hesitate to ask"
]

message = []


SystemChatBot = [{"role": "system", "content": f"Hello I'm {os.environ['Username']}, You're a content wirter. You have to write content like letter"}]


def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    def OpenNotepad(File):
        default_text_editor= 'notepad.exe'
        subprocess.Popen([default_text_editor])


    def ContentWriterAI(prompt):
        message.append({"role": "user", "content": f"{prompt}"})


        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + message,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content


        Answer = Answer.replace("</s>", "")
        message.append({"role": "assistant", "content": Answer})
        return Answer
    
    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)


    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/result?search_query={Topic}"
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

        def extra_links(html):
            if html is None:
                return[]
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [links.get('herf')for link in links]
        
        def search_google(quey):
            url = f"https://www.google.com/search?q={quey}"
            header = {"User-Agent": useragent}
            response = sess.get(url, headers=header)

            if response.status_code == 200:
                return response.txt
            else:
                print("Failed to retrive search")
            return None
        html = search_google(app)

        if html:
            links = extra_links(html)[0]
            webopen(links)

        return True

def CloseApp(app):

    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False
        
def System(command):


    def mute():
        keyboard.parse_and_release("volume mute")


    def unmute():
        keyboard.parse_and_release("volume mute")
        
    def volume_up():
        keyboard.parse_and_release("volume up")

    def volume_down():
        keyboard.parse_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True

async def TranslateAndExecute(command: list[str]):

    funcs = []

    for command in command:

        if command.startswith("open "):

            if "open it" in command:
                pass

            if "open file" == command:
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass

        elif command.startswith("realtime "):
            pass

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search"))
            funcs.append(fun)
            
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search"))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system"))
            funcs.append(fun)

        else:
            print("No functions found. For {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(results, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):
        pass
    return True

# End of automation
