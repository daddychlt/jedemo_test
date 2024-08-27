from kivy.animation import Animation
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.core.audio import SoundLoader

Builder.load_file('accueil.kv')


class AccueilScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.jedemo_label.bind(on_touch_down=self.animate_label)

    def animate_label(self, instance, touch):
        if self.ids.jedemo_label.collide_point(*touch.pos):
            animation = Animation(font_size=70, duration=0.5) + Animation(font_size=50, duration=0.5)
            animation.start(self.ids.jedemo_label)


    def go_to_game(self, instance):
        self.manager.current = 'game'  # Affiche l'écran de jeu

    def show_history(self, instance):
        print("Historique")

    def go_to_setting(self, instance):
        self.manager.current = 'setting'

