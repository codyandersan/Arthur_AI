print("Getting Assistant Ready.....\n")
import Brain
from json import load, loads
import sensors
from prediction import Predictor
from random import choice
import pygame  # For playing song
import os

song_folder = r"F:\PRAKHAR\songs" #Configure according to your project
wakeword = "arthur"
predictor = Predictor()
with open("data/responses.json") as f:
    response = loads(f.read())
brain = Brain.brain()
sense = sensors.Sensors()
ignore_words = [",", ".", "'s", wakeword, "?", "!"]


def say(text):
    print(text.title())
    sense.speak(text)


# Open cmd and type taskkill /im python.exe /t /f    if it hangs!
def hear_and_perform():
    query = sense.hear()
    if query == None: hear_and_perform()
    intent = ""
    raw_intent = predictor.predict(query.lower())
    for i in raw_intent:
        if i not in ignore_words:
            intent += i

    print(f"\nYou Said: {query}")

    # Some hardcode because it cannot be predicted for some reasons...

    if brain.if_in(["hi", "hello", "hola", wakeword, "namaste"], query):
        say(choice(response["responses"]["greeting"]).title())

    elif brain.if_in(["nothing", "shut up", "bye", "break"], query):
        say(choice(response["responses"]["break"]).title())

    elif "answer" in query and "life" in query:
        say("The answer to life, universe and everything is 42")
    elif brain.if_in(["stop", "pause"], query) and brain.if_in(
        ["song", "music", "sound"], query
    ):
        pygame.mixer.music.stop()
        say("song stopped!")

    # Intent Checking :--

    elif intent == "functions":
        ans = brain.get_all_functions()
        say(ans)

    elif intent == "time":
        ans = brain.get_time()
        say(ans)

    elif intent == "wolfram":
        say(choice(response["responses"]["wolfram"]).title())
        ans = brain.answer(query)
        say(ans)

    elif intent == "wikipedia":
        say(choice(response["responses"]["wikipedia"]).title())
        ans = brain.search_wiki(query)
        say(ans)

    elif intent == "maps":
        say(choice(response["responses"]["maps"]).title())
        brain.get_maps(query)

    elif intent == "weather":
        say("please tell the city name.")
        city = sense.hear()
        say(choice(response["responses"]["weather"]).replace("city", city).title())
        ans = brain.find_weather(city)
        temp = ans["Current Temperature"]
        place = ans["place"]
        say(f"It is {temp} in {place}.")

    elif intent == "news":
        say(choice(response["responses"]["news"]).title())
        brain.find_news()

    elif intent == "website":
        say(choice(response["responses"]["website"]).title())
        brain.open_website(query)

    elif intent == "screenshot":
        say("taking screenshot")
        brain.take_screenshot()
        say("done.")

    elif intent == "joke":
        say(choice(response["responses"]["joke"]).title())
        start, end = brain.get_joke()
        say(start)
        say(end)

    elif intent == "timegreeting":
        ans = brain.greet_with_time()
        say(ans)
    elif intent == "health":
        say(choice(response["responses"]["health"]).title())

    elif intent == "shut_down":
        say(choice(response["responses"]["shut_down"]).title())
        brain.shut_down()

    elif intent == "type":
        say("okay, please tell me what to type sentence by sentence.")
        say("you can say 'stop typing' to make me stop typing.")
        sentence = ""
        while True:
            sentence = sense.hear()
            if "stop" not in sentence:
                print("Typing: " + sentence)
                brain.type(sentence)
            else:
                break
        say("Typing stopped!")

    elif intent == "song":
        assistant_called = False
        files = [
            song
            for song in os.listdir(song_folder)
            if song.endswith(".mp3") or song.endswith(".wav")
        ]
        song = choice(files)
        song_path = song_folder + "\\" + song
        song_name = song.replace(".mp3", "").replace(".wav", "")
        pygame.mixer.music.load(song_path)
        say(f"playing {song_name}")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if sense.woke_up():
                pygame.mixer.music.pause()
                say(choice(response["responses"]["wakeup"]).title() + "\n")
                hear_and_perform()
                pygame.mixer.music.unpause()
            else:
                pygame.event.wait()
        pygame.mixer.music.stop()

    elif intent == "about_us":
        say("i am created by prakhar aditya tripathi and tanmay patel")

    elif intent == "about_me":
        ans = brain.who_am_I()
        say(ans)

    elif intent == "kill":
        say("I hope that we will meet again soon!")
        brain.kill_me()

    elif intent == "thank":
        say(choice(response["responses"]["thank"]).title())

    else:
        say("I can't figure out what you asked.")


# End of hear_and_perform

if __name__ == "__main__":
    print(
        "Hello Sir, What can I do for you?\n(BTW, You can ask me 'What can you do' to get all my functions)\n"
    )

    while True:
        if sense.woke_up():
            say(choice(response["responses"]["wakeup"]).title() + "\n")
            hear_and_perform()
        else:
            continue
