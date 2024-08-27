import json


class Enigme:
    def __init__(self, current_theme_index):
        self.current_theme_index = current_theme_index
        with open('data.json') as f:
            data = json.load(f)
        self.themes = data['themes'][self.current_theme_index]
        self.theme = self.themes['theme']
        self.letters = self.themes['letters']
        self.word = self.themes['word']
        self.hint = self.themes['hint']
