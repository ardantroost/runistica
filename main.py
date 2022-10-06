import kivy

#from kivy.config import Config

#Config.set('graphics', 'width',350)
#Config.set('graphics', 'height',700)
#Config.set('graphics', 'resizable',1)

from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

#foutmelding als je kv file (van runenmaster) laadt met alle screens

Builder.load_file("welcome.kv")
Builder.load_file("menu.kv")
Builder.load_file("quizz.kv")
Builder.load_file("vragen.kv")
Builder.load_file("vrageneen.kv")
Builder.load_file("vragentwee.kv")
Builder.load_file("result.kv")
Builder.load_file("collegesymbols.kv")
Builder.load_file("collegenames.kv")
Builder.load_file("stats.kv")


class RunenMasterScreens(ScreenManager):

    # op te roepen Popup in de hele APP
    # call met:   self.manager.Popup_choose(alarmtype)
    # alarmtype om mee te geven: training, antwoord

    def Popup_Choose(self,alarmtype):
        self.PopupPressed = Popup(title="Warning",
                                  separator_color=[0, 1, 0, .6],
                                  content= Label(text=f"Please choose {alarmtype}", halign="center", font_size=24),
                                  size_hint=(None, None),
                                  size=(400, 300),
                                  pos_hint={"center_x": .5, "center_y": .5},
                                  background_color=[0, 1, 0, .6],
                                  auto_dismiss=True)
        self.PopupPressed.open()

class MainApp(App):
    def build(self):
        # 256 x 256 pixels
        #self.icon = "icon.png"
        return RunenMasterScreens()

if __name__ == '__main__':

    MainApp().run()



