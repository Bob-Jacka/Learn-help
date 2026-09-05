"""
Listen to question instead of seeing it
"""
import os

try:
    import pyttsx3
    from gtts import gTTS
    import gtts
except ModuleNotFoundError as e:
    print(f'No available tts found: {e}')


class Norator:
    def __init__(self, words_per_minute: int, volume: float, offline_mode: bool = True):
        """
        Construct norator to norate question
        :param offline_mode: is use for local functionality
        """
        self.norator_mode = offline_mode
        if offline_mode:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', words_per_minute)
            self.engine.setProperty('volume', volume)
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'ru' in voice.languages or 'Russian' in voice.name:
                    self.engine.setProperty('voice', voice.id)
                    break
        else:
            self.engine = None
            pass

    def available_languages(self) -> list | dict:
        """
        Get available languages for engine
        :return:
        """
        if self.norator_mode:
            voices = self.engine.getProperty('voices')
            return [x for x in voices.languages]
        else:
            return gtts.langs

    def norate_string(self, text_to_norate: str):
        if self.norator_mode:  # offline branch
            self.engine.say(text_to_norate)
            self.engine.runAndWait()

        else:  # if not offline mode
            self.engine = gTTS(text=text_to_norate, lang='ru')
            self.engine.save("output.mp3")
            os.system('mpg123 output.mp3')
