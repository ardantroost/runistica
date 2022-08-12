import kivy
from kivy.uix.label import Label
kivy.require("2.1.0")
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

#foutmelding als je kv file (van runenmaster) laadt met alle screens

Builder.load_file("welcome.kv")
Builder.load_file("menu.kv")
Builder.load_file("quizz.kv")
Builder.load_file("vragen.kv")
Builder.load_file("vragen_1.kv")
Builder.load_file("vragen_2.kv")
Builder.load_file("result.kv")
Builder.load_file("collegesymbols.kv")
Builder.load_file("collegenames.kv")


class RunenMasterScreens(ScreenManager):

    # op te roepen Popup in de hele APP
    # call met:   self.manager.Popup_choose(alarmtype)
    # alarmtype om mee te geven: training, antwoord

    def Popup_Choose(self,alarmtype):
        self.PopupPressed = Popup(title="Warning",
                                  separator_color=[0, 1, 0, .6],
                                  content= Label(text=f"Please choose {alarmtype}", halign="center", font_size=13),
                                  size_hint=(None, None),
                                  size=(200, 100),
                                  pos_hint={"center_x": .5, "center_y": .5},
                                  background_color=[0, 1, 0, .6],
                                  #background="Pics/eye.png",
                                  auto_dismiss=True)
        self.PopupPressed.open()

class MainApp(App):
    def build(self):
        # 256 x 256 pixels
        self.icon = "icon.png"
        return RunenMasterScreens()

if __name__ == '__main__':

    MainApp().run()



