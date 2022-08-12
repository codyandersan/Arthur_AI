# if it says to download ne_chunk or any other nltk package, do in interpreter:
# import nltk
# nltk.download("--Name of missing package--")


from requests import get #for wolframalpha sesarch api
from nltk.tokenize import word_tokenize #create a list of words in a sentence
from nltk import ne_chunk, pos_tag #Detect the name of a person in a sentence
from datetime import datetime
import wikipedia
from webbrowser import open as launch
import weather
from random import choice, randint
from newsapi import NewsApiClient
from json import load, dump
from googlesearch import search as find_urls #To do google search
from pyautogui import screenshot, write, press
from time import sleep
import pygame #For playing songs
import os
from sys import exit
from re import sub # to remove text in brackets in wiki summary


pygame.init()
pygame.mixer.init()

song_folder = r"F:\PRAKHAR\songs" #replace with yours


class brain:
    def __init__(self):
        app_id = "R2K75H-7ELALHR35X"

    def who_am_I(self):
        return choice(
            [
                "i am Arthur, your personal assitant",
                "how can you forget me? i am arthur",
                "oh! don't you know who am I. i am arthur",
            ]
        )

    def get_all_functions(self):
        functions = [
            [
                "solve x+2=7",
                "what is the answer of 1 + 2",
                "find out x^2 + 2x - 3 = 0",
            ],
            [
                "how many calories are there in a banana?",
                "how much fat is in papaya",
                "how much energy does an orange gives",
            ],
            ["who is Amitabh Bachchan?", "who is Johnny Lever?", "who is Salman Khan?"],
            [
                "where is Bhopal?",
                "where is Denmark?",
                "where on earth is England?",
                "show me the map of India",
            ],
            [
                "How is the weather in Nagpur?",
                "do I need an umbrella today?",
                "is it cold outside?",
            ],
            [
                "Play the current news",
                "tell me the news",
                "what are the current news headlines",
            ],
            ["Open Twitter", "open Facebook", "launch Instagram"],
            ["Take a screenshot", "Capture the screen "],
            ["Tell me the time", "tell me the current time"],
            ["Play some music", "play a song"],
            ["Tell me a joke", "Make me laugh", "Can you make me laugh?"],
        ]
        rand_function = choice(functions)
        rand_function = choice(rand_function)
        return f"Try Saying: {rand_function}"

    def get_wakewords(self):
        with open("data/wakewords.txt") as file:
            wakewords = file.readlines()
            return wakewords

    def add_wakeword(self, wakeword):
        wakewords = self.get_wakewords()
        with open("data/wakewords.txt", "a") as file:
            if wakeword not in wakewords:
                file.write(wakeword.lower() + "\n")

    def tokenize(self, s):
        return word_tokenize(s)

    def if_in(self, valid_items, list):
        list = self.tokenize(list)
        for item in valid_items:
            if item in list:
                return True
        else:
            return False

    def checkiflist(self, variable):
        if isinstance(variable, list):
            return variable[0]["plaintext"]
        else:
            return variable["plaintext"]

    def get_names(self, st):
        if isinstance(st, list) == False:
            word = self.tokenize(st)
        else:
            word = st
        tag = pos_tag(word)
        parsed = ne_chunk(tag, binary=True)
        listy = list(
            " ".join(i[0] for i in t)
            for t in parsed
            if hasattr(t, "label") and t.label() == "NE"
        )
        z = ""
        for i in listy:
            z = z + " " + i
        return z

    def get_time(self):
        return (
            "It is "
            + str(datetime.now().strftime("%H:%M:%S"))
            + " on "
            + str(datetime.now().strftime("%d|%m|%Y"))
        )

    def answer(self, question):

        link = f"https://api.wolframalpha.com/v1/result?i={question}&appid=R2K75H-7ELALHR35X"
        answer = get(link)
        if answer.status_code != 200:
            question = question.replace(" ", "+")
            launch(f"https://www.google.com/search?q={question}")
            return "searching google..."
        else:
            return answer.text

    def search_wiki(self, term):
        name = self.get_names(term)
        try:
            summary = wikipedia.summary(name, sentences=1)
        except wikipedia.DisambiguationError as e:
            summary = wikipedia.summary(e.options[0], sentences=1)
        except:
            summary = self.answer(term)
        sub(r"[\(\[].*?[\)\]]", "", summary)
        return summary

    def get_maps(self, query):

        location = self.get_names(query)
        launch(f"https://www.google.nl/maps/place/{location}")
        return location

    def greeter(self, greet, type):
        if type == "bye":
            exit("Thank you for your time. See you soon!")
        elif type == "greet":
            mygreets = ["Hello Sir", "Hi", "How can I help you?"]
            return f"{choice(mygreets)}"
        elif type == "angry":
            return "Sorry Sir. I am not yet so advanced."

    def find_weather(self, city):
        dict = weather.get_weather(city, "1")
        return dict

    def find_news(self):
        return_dict = []
        client = NewsApiClient(api_key="e611204d9f10403abdedb30899889aae")
        api = client.get_top_headlines(language="en", country="in")
        for news in api["articles"]:
            return_dict.append(
                {
                    "source": news["source"]["name"],
                    "content": news["title"],
                    "url": news["url"],
                }
            )
        return return_dict

    def open_website(self, query):
        web = self.get_names(query).lower().strip()
        if web == "":
            web = (
                query.lower()
                .replace("open", "")
                .replace("launch", "")
                .replace("start", "")
                .replace(" ", "")
            )
        websites = load(open("websites.json"))
        if web not in websites:
            links = []
            for x in find_urls(
                query=web + " official website",
                tld="com",
                num=3,
                stop=3,
                pause=3,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            ):
                links.append(x)
            link = links[0]
            websites.update({web: link})
            dump(websites, open("websites.json", "w"))
            launch(link)
        else:
            launch(websites[web])

    def take_screenshot(self):
        prefix = str(datetime.now().strftime('%H|%M|%S'))
        screenshot(f"screenshot_{prefix}.jpg")

    def get_joke(self):
        with open("data/jokes.json") as f:
            jokes = load(f)
        joke_id = randint(1, 387)
        joke = jokes[joke_id]
        return [joke["setup"], joke["punchline"]]

    def greet_with_time(self):
        if (
            datetime.now().strftime("%H") < "12"
            and datetime.now().strftime("%H") > "00"
        ):
            return "Good Morning Sir, What can i do for you?"
        elif datetime.now().strftime("%H") == "12":
            return "Good Noon Sir, What can i do for you?"
        elif (
            datetime.now().strftime("%H") > "12"
            and datetime.now().strftime("%H") < "16"
        ):
            return "Good Afternoon Sir, What can i do for you?"
        elif (
            datetime.now().strftime("%H") > "16"
            and datetime.now().strftime("%H") < "00"
        ):
            return "Good Evening Sir, What can i do for you?"

    def kill_me(self):
        exit()

    def shut_down(self):
        self.kill_me()
        os.system("shutdown /s")

    def type(self, text):
        write(text)
        press("space")
