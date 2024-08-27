from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from accueil import AccueilScreen
from end_game import EndGameScreen
from game import GameScreen
from pre_splash import PreSplashScreen


#from setting import SettingScreen

class MainApp(MDApp):
    def build(self):

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "200"

        self.screen_manager = MDScreenManager()
        self.all_themes_completed = False

        #Window.size_hint = (None, None)  # To ensure responsiveness
        #Window.size = (300, 600)  # To ensure responsiveness
        #self.size = Window.size  # To ensure responsiveness

        # Ajout des différentes pages au ScreenManager
        self.screen_manager.add_widget(PreSplashScreen(name="pre_splash"))
        self.screen_manager.add_widget(AccueilScreen(name='accueil'))
        self.screen_manager.add_widget(GameScreen(name='game'))
        self.screen_manager.add_widget(EndGameScreen(name='end_game'))
        #self.screen_manager.add_widget(SettingScreen(name='setting'))

        return self.screen_manager


if __name__ == "__main__":
    MainApp().run()
