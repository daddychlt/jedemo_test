import random
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from colors import liste_color

Builder.load_file("pre_splash.kv")

class PreSplashScreen(Screen):

    global liste_colors
    liste_colors = [keys for keys in liste_color]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.show_progressbar, 3)
        self.start_time = None

    def show_progressbar(self, dt):
        self.ids.loadingText.opacity = 1
        self.ids.loadingProgress.opacity = 1
        if self.ids.loadingProgress.opacity == 1:
            self.start_time = Clock.get_time()  # Enregistre le temps de début
            self.clock = Clock.schedule_interval(self.update_progressbar, 0.05)  # Mise à jour toutes les 0.05 secondes

    def update_progressbar(self, dt):
        if self.start_time is not None:
            elapsed_time = Clock.get_time() - self.start_time
            progress = min(elapsed_time / 9.0 * 100, 100)  # Calcule le pourcentage de progression en 9 secondes

            self.ids.loadingProgress.value = progress
            self.ids.loadingProgress.color = liste_colors[int(elapsed_time / 2) % len(liste_colors)]

            self.ids.loadingText.text = "Chargement" + "." * (int(elapsed_time) % 4)

            if progress >= 100:
                self.clock.cancel()  # Arrête la mise à jour
                Clock.schedule_once(self.transition_to_home, 2)  # Attends 1 seconde avant la transition
        else:
            self.start_time = Clock.get_time()  # Redémarre le chronomètre si nécessaire

    def transition_to_home(self, dt):
        self.manager.current = 'accueil'
