import webbrowser
import time

# Try to import optional dependencies and record missing ones
_missing_deps = []

try:
    import speech_recognition as sr
except Exception:
    sr = None
    _missing_deps.append('SpeechRecognition')

try:
    import pyttsx3
except Exception:
    pyttsx3 = None
    _missing_deps.append('pyttsx3')

try:
    import pyautogui
except Exception:
    pyautogui = None
    _missing_deps.append('pyautogui')

try:
    import pytesseract
except Exception:
    pytesseract = None
    _missing_deps.append('pytesseract')

try:
    from PIL import Image
except Exception:
    Image = None
    _missing_deps.append('Pillow')

try:
    import openai
except Exception:
    openai = None
    _missing_deps.append('openai')

# Provide a safe speak() fallback if pyttsx3 is not available
if pyttsx3 is not None:
    engine = pyttsx3.init()

    def speak(text):
        engine.say(text)
        engine.runAndWait()
else:
    def speak(text):
        # Simple console fallback
        print("[Jarvis]", text)

# If critical module is missing, give instructions and exit gracefully
if 'SpeechRecognition' in _missing_deps or pyttsx3 is None:
    msg_lines = [
        "Missing Python dependencies detected.",
        "Install required packages with:",
        "  python -m pip install -r requirements.txt",
        "On Windows, install PyAudio via pipwin if needed:",
        "  python -m pip install pipwin",
        "  python -m pipwin install pyaudio",
        "Also install Tesseract OCR separately for pytesseract to work:",
        "  https://github.com/tesseract-ocr/tesseract",
        "Detected missing: " + ", ".join(_missing_deps),
    ]
    for l in msg_lines:
        print(l)
    # try to speak the first line if possible
    try:
        speak(msg_lines[0])
    except Exception:
        pass
    # Exit so the user can install dependencies
    raise SystemExit(1)


 
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        speak("Say that again?")
        return ""



def take_screenshot():
    image = pyautogui.screenshot()
    image.save("screen.png")
    speak("Screenshot taken.")



def read_screen():
    image = pyautogui.screenshot()
    image.save("screen_read.png")
    text = pytesseract.image_to_string(Image.open("screen_read.png"))
    speak(text)


def open_app(app_name):
    if "youtube" in app_name:
        webbrowser.open("https://youtube.com")
    elif "chatgpt" in app_name:
        webbrowser.open("https://chat.openai.com")
    else:
        speak("I don't know this app yet.")



def type_text(text):
    pyautogui.write(text, interval=0.05)



if __name__ == "__main__":
    speak("Jarvis activated.")

    while True:
        command = listen()

        if "screenshot" in command:
            take_screenshot()

        elif "read screen" in command or "read the screen" in command:
            read_screen()

        elif "open" in command:
            app = command.replace("open", "").strip()
            open_app(app)

        elif "type" in command:
            text = command.replace("type", "").strip()
            type_text(text)

        elif "stop" in command or "bye" in command:
            speak("Goodbye.")
            break