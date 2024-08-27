import json

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton
from nltk import edit_distance

import donnees as dn

Builder.load_file('game.kv')


class MagicButton(MagicBehavior, MDRaisedButton):
    pass


class GameScreen(Screen):

    global liste_reperage_boutns

    liste_reperage_boutns = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recompense = False
        self.current_theme_index = 0
        self.enigme = dn.Enigme(self.current_theme_index)
        self.game()

    # fonction de chargement
    def game(self):
        # Charger le thème courant
        themes = self.get_themes()

        # Vérifier si nous avons encore des thèmes à parcourir
        if self.current_theme_index < len(themes):

            self.enigme = dn.Enigme(self.current_theme_index)  # Charger le nouvel enigme

            self.ids.progress.value = self.ids.progress.value + 5   # Afficher le thème
            self.ids.level.text = self.enigme.theme  # Afficher le thème
            self.ids.indice.text = self.enigme.hint  # Afficher l'indice
            self.ids.texte.text = "_"  # Réinitialiser le texte affiché

            # Réinitialiser les boutons
            self.ids.bouton_box.clear_widgets()
            for letter in self.enigme.letters:
                button = Button(text=letter.upper(), on_release=self.display_letter)
                button.disabled = False
                self.ids.bouton_box.add_widget(button)

        else:
            # Si nous avons parcouru tous les thèmes, finir le jeu ou recommencer
            self.go_to_end()



    def display_letter(self, instance):
        if not self.recompense:
            current_text = self.ids.texte.text
            if current_text.endswith("_"):
                current_text = current_text[:-1]  # Remove the underscore if it's at the end
            self.ids.texte.text = current_text + instance.text + "_"
            instance.disabled = True
            liste_reperage_boutns.append(instance)

    def erase_letter(self, instance):
        if not self.recompense:
            current_text = self.ids.texte.text
            if current_text.endswith("_"):
                current_text = current_text[:-1]  # Remove the underscore if it's at the end
            if len(current_text) > 0:
                self.ids.texte.text = current_text[:-1] + "_"
            if len(liste_reperage_boutns) > 0:
                bouton = liste_reperage_boutns[len(liste_reperage_boutns)-1]
                bouton.disabled = False
                liste_reperage_boutns.remove(bouton)

    def delete_word(self, instance):
        if not self.recompense:
            for bouton in liste_reperage_boutns:
                bouton.disabled = False
            liste_reperage_boutns.clear()

            self.ids.texte.text = "_"

    def verifier_proximite(self, mot_ecrit, mot_a_deviner):
        seuil = 2  # Seuil de distance pour considérer les mots comme proches
        distance = edit_distance(mot_ecrit, mot_a_deviner)

        if distance <= seuil:
            self.ids.prox.text = "Vous êtes proche"
        else:
            self.ids.prox.text = "Essayer encore"
        (Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)).start(self.ids.prox)

    def validate_word(self, instance):
        if not self.recompense:
            current_text = self.ids.texte.text
            if len(current_text) > 1:
                if current_text[:-1] == self.enigme.word:
                    self.ids.texte.text = current_text[:-1]
                    self.ids.texte.color = "green"
                    Clock.schedule_once(self.recompense_come, 1)  # Planifier la restauration après 5 secondes

                else:
                    self.ids.texte.color = "red"
                    self.verifier_proximite(current_text, self.enigme.word)
                    self.ids.texte.text = current_text[:-1]  # Enlever la dernière lettre
                    Clock.schedule_once(self.restore_text, 1)  # Planifier la restauration après 5 secondes


    def restore_text(self, dt):
        self.ids.texte.color = "black"  # Remettre la couleur originale, ajustez si nécessaire
        current_text = self.ids.texte.text
        self.ids.texte.text = current_text + "_"  # Ajouter un curseur à la fin du texte

    def next_theme(self, instance):
        self.recompense_back(instance)
        self.ids.texte.color = "black"  # Remettre la couleur originale
        self.ids.texte.text = "_"

        self.current_theme_index += 1

        # Charger le prochain mot/thème
        self.game()

    def get_themes(self):
        with open('data.json') as f:
            data = json.load(f)
        return data['themes']

    def recompense_come(self, instance):
        self.recompense = True
        self.ids.grid.opacity = .5
        liste_reperage_boutns.clear()
        (Animation(pos_hint={"center_y": 0.5}, duration=0.2) + Animation(size=[dp(250), dp(100)], duration=0.2) + Animation( size=[dp(200), dp(250)], duration=0.2)).start(self.ids.recompense)
        Animation(pos_hint={"center_y": 0.6}, duration=0.3).start(self.ids.center_crown)
        Animation(pos_hint={"center_x": 0.3, "center_y": .55}, duration=0.3).start(self.ids.left_crown)
        Animation(pos_hint={"center_x": 0.7, "center_y": .55}, duration=0.3).start(self.ids.right_crown)
        Clock.schedule_once(self.start_progress, 1)

    def start_progress(self, dt):
        # Augmenter la valeur cible
        target_value = min(self.ids.progress_rep.value + 5, 100)  # S'assurer que la valeur ne dépasse pas 100

        self.ids.progress_rep.opacity = 1
        # Animation fluide pour passer de la valeur actuelle à la valeur cible
        animation = Animation(value=target_value, duration=1)  # Ajuster la durée pour plus de fluidité
        animation.start(self.ids.progress_rep)

    def recompense_back(self, instance):
        self.ids.grid.opacity = 1
        self.recompense = False
        self.ids.progress_rep.opacity = 0
        Animation(pos_hint={"center_y": 1.5}, duration=0.2).start(self.ids.recompense)


    def go_to_home(self, instance):
        self.manager.current = 'accueil'

    def go_to_end(self):
        self.manager.current = 'end_game'