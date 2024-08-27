from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_file('end_game.kv')


class EndGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Exécute l'animation après 1 seconde
        Clock.schedule_interval(self.animate_end_screen, 1)

    def animate_end_screen(self, dt):
        # Animation de la taille des étoiles
        anim = Animation(font_size=dp(130), duration=0.5) + Animation(font_size=dp(100), duration=0.5)
        anim.start(self.ids.reward_icon)

    def go_to_home(self, instance):
        self.manager.current = 'accueil'
