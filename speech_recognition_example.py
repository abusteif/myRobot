import speech_recognition
import pyttsx3
from num2words import num2words
from subprocess import call


cmd_beg= 'espeak '
cmd_end= ' | aplay /home/pi/Desktop/Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
cmd_out= '--stdout > /home/pi/Desktop/Text.wav ' # To store the voice file

recognizer = speech_recognition.Recognizer()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic, phrase_time_limit=3)
            text = recognizer.recognize_google(audio)
            text = text.lower()
            text = text.replace(' ', '_')

            call([cmd_beg+cmd_out+text+cmd_end], shell=True)
            if "quit" in text:
                exit(1)
            print(f"Recognized {text}")
            
        
    except speech_recognition.UnknownValueError as e:
        print("aaaa")
        recognizer = speech_recognition.Recognizer()
        pass