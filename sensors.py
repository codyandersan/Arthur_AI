# Make sure that you are connected to internet before running this!!!

import speech_recognition as sr
import pyttsx3
from sys import platform

with open("data/wakewords.txt") as file:
    wakewords = file.readlines()
    wakewords = [x.replace("\n", "") for x in wakewords]


class Sensors:
    def __init__(self):
        try:
            if platform == "win32": # main apne par ek custom voice lagaya hu that's why
                self.eng = pyttsx3.init()
                self.eng.setProperty("rate", 150)
                self.r = sr.Recognizer()
                self.mic = sr.Microphone(device_index=1)
                self.voices = self.eng.getProperty("voices")
                self.eng.setProperty("voice", self.voices[3].id)

            else: # aapke system ke liye
                self.eng = pyttsx3.init()
                self.eng.setProperty("rate", 150)
                self.r = sr.Recognizer()
                self.mic = sr.Microphone(device_index=1) #1 or 0 mein se koi hoga
                
        except:
            print("Failed to Initialize!")

    # Open cmd and type taskkill /im python.exe /t /f    if it hangs!
    def woke_up(self):
        try:
            while True:
                with self.mic as s:
                    self.r.adjust_for_ambient_noise(s)
                    audio = self.r.listen(s, phrase_time_limit=1.5)
                x = self.r.recognize_google(audio)
                for item in wakewords:
                    if item in x.lower():
                        break
                if x.lower() in wakewords:
                    break

            return True
        except:
            self.woke_up()

    def hear(self):
        with self.mic as s:
            self.r.adjust_for_ambient_noise(s)
            audio = self.r.listen(s)
        try:
            x = self.r.recognize_google(audio)
            return x
        except:
            self.speak("can you say that again?")
            self.hear()


    def speak(self, text):
        self.eng.say(text)
        self.eng.runAndWait()
