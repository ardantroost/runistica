from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.popup import Popup

Config.set('graphics', 'width',350)
Config.set('graphics', 'height',600)
Config.set('graphics', 'resizable',0)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

#foutmelding als je kv file (van runenmaster) laadt met alle screens
#Builder.load_file("runenmaster.kv")
Builder.load_file("welcome.kv")
Builder.load_file("menu.kv")
Builder.load_file("quizz.kv")
Builder.load_file("vragen.kv")
Builder.load_file("vragen_1.kv")
Builder.load_file("vragen_2.kv")
Builder.load_file("result.kv")
Builder.load_file("CollegeSymbols.kv")
Builder.load_file("CollegeNames.kv")
Builder.load_file("dashboard.kv")

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
                                  background_color=[0, 1, 0, 1],
                                  background="Pics/eye.png",
                                  auto_dismiss=True)
        self.PopupPressed.open()


class RunenMasterApp(App):
    def build(self):
        return RunenMasterScreens()

if __name__ == '__main__':
    RunenMasterApp().run()



