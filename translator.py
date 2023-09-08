from googletrans import Translator
from gtts import gTTS
import pygame
import os
import speech_recognition as sr


class Translation:
    def __init__(self):
        self.translator = Translator()
        self.recognizer = sr.Recognizer()
        self.language_dict = {"arabic": "ar", "bengali": "bn", "chinese": "zh", "czech": "cs", "danish": "da",
                              "dutch": "nl", "english": "en", "finnish": "fi", "french": "fr", "german": "de",
                              "greek": "el", "gujarati": "gu", "hindi": "hi", "hungarian": "hu", "italian": "it",
                              "japanese": "ja", "kannada": "kn", "korean": "ko", "malayalam": "ml", "marathi": "mr",
                              "norwegian": "no", "portuguese": "pt", "punjabi": "pa", "russian": "ru", "spanish": "es",
                              "swedish": "sv", "tamil": "ta", "telugu": "te", "turkish": "tr", "urdu": "ur"}

    def translate_text(self, text, code):
        translated_text = self.translator.translate(text, dest=code)
        return translated_text.text

    def speak_text(self, text, code):
        tts = gTTS(text, lang=code)
        audio_file_path = "translated_audio.mp3"
        tts.save(audio_file_path)
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        os.remove(audio_file_path)

    def speech_to_text(self, code):
        global in_code
        recognizer = sr.Recognizer()
        allow = True
        while allow:
            in_lang = input("\nEnter the input language:")
            if in_lang.lower() in self.language_dict:
                print(f"You have selected {in_lang.upper()}")
                in_code = self.language_dict[in_lang.lower()]
                allow = False
            else:
                print("It's not a valid language/language not available!")
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            recognized_text = recognizer.recognize_google(audio, language=in_code)
            print("Recognized Text:", recognized_text)
            translator = Translator()
            translated_text = translator.translate(recognized_text, dest=code)
            return translated_text.text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    def main(self):
        global user_code
        allow = True
        while allow:
            user_lang = input("\nPlease enter the desired language:")
            if user_lang.lower() in self.language_dict:
                print(f"You have selected {user_lang.upper()}")
                user_code = self.language_dict[user_lang.lower()]
                allow = False
            else:
                print("It's not a valid language/language not available!")

        while True:
            choice = input("\nChoose an option:\n1. Text Translation\n2. Speech to Text Translation\n3. Exit\n")

            if choice == "1":
                text_to_translate = input("\nWrite the text you want to translate:\n"
                                          "To return to the menu, write 'menu'\n")
                if text_to_translate.lower() == "menu":
                    continue
                translated_text = self.translate_text(text_to_translate, user_code)
                print(translated_text)
                convert_to_speech = input("Do you want to convert the translated text to speech? (yes/no): ")
                if convert_to_speech.lower() == "yes":
                    self.speak_text(translated_text, user_code)

            elif choice == "2":
                translated_text = self.speech_to_text(user_code)
                if translated_text:
                    print(translated_text)
                    convert_to_speech = input("Do you want to convert the translated text to speech? (yes/no): ")
                    if convert_to_speech.lower() == "yes":
                        self.speak_text(translated_text, user_code)

            elif choice == "3":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    app = Translation()
    app.main()