# Arthur AI

A voice-activated personal assistant for Windows, built in Python. Arthur listens for a wake word, recognises your spoken command, classifies the intent using a trained Naive Bayes model, and responds with both text output and synthesized speech.

---

## Features

| Capability | Example Commands |
|---|---|
| **Q&A / Math** (WolframAlpha) | "solve x² + 2x - 3 = 0", "what is 1 + 2" |
| **Wikipedia search** | "who is Amitabh Bachchan?", "who is Salman Khan?" |
| **Weather** | "how is the weather in Nagpur?", "is it cold outside?" |
| **News headlines** | "tell me the news", "play the current news" |
| **Maps** | "where is Denmark?", "show me the map of India" |
| **Open websites** | "open Twitter", "launch Instagram" |
| **Play music** | "play a song", "play some music" |
| **Stop music** | "stop the song", "pause music" |
| **Tell the time** | "tell me the time", "what time is it?" |
| **Tell a joke** | "tell me a joke", "make me laugh" |
| **Take a screenshot** | "take a screenshot", "capture the screen" |
| **Type text** | "type a message" (dictates text via pyautogui) |
| **Shutdown PC** | "shut down" |
| **Greetings** | "hi", "hello", "namaste" |
| **What can you do?** | "what can you do?" |

---

## Architecture

```
Arthur_AI/
├── main.py           # Entry point — wake word loop + intent dispatcher
├── Brain.py          # All capability implementations (weather, wiki, jokes, etc.)
├── sensors.py        # Speech input (STT) and speech output (TTS)
├── prediction.py     # Naive Bayes intent classifier (trained on intents.csv)
├── weather.py        # WeatherAPI wrapper — returns full weather + astronomy data
├── data/
│   ├── intents.csv   # Training data for the intent classifier
│   ├── responses.json# Randomized spoken responses per intent
│   ├── jokes.json    # Joke dataset (setup + punchline)
│   └── wakewords.txt # List of wake words that activate Arthur
└── requirements.txt  # Python dependencies
```

**How it works:**

1. `sensors.py` continuously listens via the microphone.
2. When a wake word from `data/wakewords.txt` is detected, Arthur activates.
3. The user's speech is transcribed using Google Speech Recognition.
4. `prediction.py` classifies the transcribed text into an intent using a TF-IDF + Multinomial Naive Bayes model trained on `data/intents.csv`.
5. `main.py` dispatches to the appropriate handler in `Brain.py`.
6. Arthur speaks the response back via `pyttsx3`.

---

## Requirements

- **Python 3.x**
- **Windows** (recommended — voice engine uses Windows SAPI voices; some paths are Windows-specific)
- A working microphone
- Internet connection (for STT, WolframAlpha, Wikipedia, Weather, News, Maps)

### API Keys Required

The following API keys are hardcoded in the source files. Replace them with your own before running:

| Key | File | Where to get it |
|---|---|---|
| WolframAlpha App ID | `Brain.py` | [developer.wolframalpha.com](https://developer.wolframalpha.com) |
| WeatherAPI Key | `weather.py` | [weatherapi.com](https://www.weatherapi.com) |
| NewsAPI Key | `Brain.py` | [newsapi.org](https://newsapi.org) |

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/codyandersan/Arthur_AI.git
cd Arthur_AI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

Some NLTK packages are also required. Run once in a Python interpreter:
```python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
```

### 3. Configure your setup

**Songs folder** — Update the `song_folder` path in both `main.py` and `Brain.py`:
```python
song_folder = r"C:\Users\YourName\Music"  # Change this
```

**Microphone index** — If Arthur doesn't hear you, try changing `device_index` in `sensors.py`:
```python
self.mic = sr.Microphone(device_index=0)  # Try 0 or 1
```

**Voice selection** — On Windows, `self.voices[3].id` selects a specific TTS voice. Change the index to match a voice installed on your system.

**Create `websites.json`** — This file is needed for the "open website" feature but is not included in the repo. Create it manually in the project root:
```json
{}
```
Arthur will populate it automatically as you ask it to open websites.

### 4. Run Arthur
```bash
python main.py
```

Arthur will print `"Hello Sir, What can I do for you?"` and start listening for the wake word **"arthur"**.

> **If Arthur hangs:** Open Command Prompt and run `taskkill /im python.exe /t /f`

---

## Adding Wake Words

Edit `data/wakewords.txt` and add one wake word per line:
```
arthur
hey arthur
assistant
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `SpeechRecognition` | Microphone input and Google STT |
| `pyttsx3` | Text-to-speech output |
| `pygame` | Music playback |
| `scikit-learn` | Intent classification (Naive Bayes) |
| `pandas` | Loading training data CSV |
| `nltk` | Tokenization and named entity recognition |
| `wikipedia` | Wikipedia summaries |
| `requests` | HTTP calls (WolframAlpha, WeatherAPI) |
| `newsapi-python` | News headlines |
| `google` | Google search for website discovery |
| `pyautogui` | Screenshot capture and keyboard typing |
| `numpy` | scikit-learn dependency |
