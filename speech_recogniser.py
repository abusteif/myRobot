import speech_recognition
import pyttsx3

class SpeechRecogniser:
    
    def __init__(self):
        
        self.recognizer = speech_recognition.Recognizer()
        
    def start_listening(self, duration):
        try:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = self.recognizer.listen(mic, phrase_time_limit=duration)
                text = self.recognizer.recognize_google(audio)
                text = text.lower()
                text = text.replace(' ', '_')
                print(text)
                return text
        except speech_recognition.UnknownValueError as e:
            self.recognizer = speech_recognition.Recognizer()
            return None
