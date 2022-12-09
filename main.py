import sqlite3
# eigen vertalingsmodule
import taal as taal
from kivmob import KivMob, TestIds
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import StringProperty,ListProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

#foutmelding als je kv-file (van runenmaster) laadt met alle screens
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
Builder.load_file("advice.kv")

class RunenMasterScreens(ScreenManager):

    def taalkeuze(self,speak):

        taal.taalknop(self,speak)


    def show_Banner(self):
        print("tijd voorrr banner-reklame")
        # admob:
        # App ID: ca-app-pub-5700178800129779~8203136809
        # ID advertblok: ca - app - pub - 5700178800129779 / 6594579659
        # test van de id ads: ca - app - pub - 3940256099942544 / 6300978111

        # self.ads = KivMob(TestIds.APP)
        self.ads = KivMob('ca-app-pub-3940256099942544~3347511713')

        # self.ads.new_banner(TestIds.BANNER,False)
        self.ads.new_banner('ca-app-pub-3940256099942544/6300978111', top_pos=False)
        self.ads.request_banner()
        self.ads.show_banner()

    def interstitial(self):
        print("tijd voor andere reklaaaaaaaaaaaaame")
        self.ads = KivMob(TestIds.APP)
        self.ads.new_interstitial(TestIds.INTERSTITIAL)
        self.ads.request_interstitial()
        self.ads.show_interstitial()



    # op te roepen Popup in de hele APP
    # call met:   self.manager.Popup_choose(alarmtype)
    # alarmtype om mee te geven: training of antwoord

    def referal(self):

        conn = sqlite3.connect("masterresults.db")
        c = conn.cursor()
        c.execute("DELETE From masterresults")
        conn.commit()
        conn.close()
        self.Popup_warning.dismiss()
        self.get_screen("statsscreen").on_enter()

    def Popup_delete_warning(self):

        self.b1 =BoxLayout(orientation="vertical",pos_hint={"center_x":0.5,"center_y":.5})
        self.b2 = BoxLayout(orientation="horizontal", size_hint=(.5,.25),spacing=40,pos_hint={"center_x":0.5,"center_y":.5})
        self.button_No= Button(text="No",halign="center",size_hint=(None,None),size=(100,50),font_size=18, color=[1,1,1,1],pos_hint={"center_x":0.45})
        self.button_Yes= Button(text="Yes", halign="center",size_hint=(None,None), size=(100,50), font_size=18,color=[1,1,1,1],pos_hint={"center_x":0.55})

        self.label_warning=Label(text="Do you really want to delete all your testscores?", halign="center",color=(1,0,1,1) ,font_size=22,text_size=(220, None))
        self.b2.add_widget(self.button_No)
        self.b2.add_widget(self.button_Yes)

        self.button_Yes.bind(on_press=lambda *args:self.referal())
        self.button_No.bind(on_press=lambda *args: self.Popup_warning.dismiss())

        self.b1.add_widget(self.label_warning)
        self.b1.add_widget(self.b2)

        self.Popup_warning = Popup(title="Warning",
                                   title_size=24,
                                  title_color=[0,0,0,1],
                                  separator_color=[1, 0, 1, .6],
                                  content=self.b1,
                                  size_hint=(None, None),
                                  size=(550, 400),
                                  pos_hint={"center_x": .5, "center_y": .5},
                                  background="",
                                  auto_dismiss=False)
        self.Popup_warning.open()

    def Popup_Practicum(self):
        self.Box=BoxLayout(orientation="vertical")
        self.Imagepop=Image(source="Pics/logorunistica.png")
        self.Labelpop=Label(text="Well Done you!", halign="center", font_size=28, color=[1,0,0,1])
        self.Box.add_widget(self.Imagepop)
        self.Box.add_widget(self.Labelpop)

        self.PopupPressed = Popup(title="",
                                  separator_color=[1, 1, 1,1],
                                  content= self.Box,
                                  size_hint=(None, None),
                                  size=(450, 450),
                                  pos_hint={"center_x": .5, "center_y": .5},
                                  background="",
                                  #background_color=[1, 1, 1,1],
                                  auto_dismiss=True)
        self.PopupPressed.open()

    def Popup_Choose(self,alarmtype):

        self.Box1 = BoxLayout(orientation="vertical")
        self.Imagepop = Image(source="Pics/logorunistica.png")
        self.Labelpop = Label(text=f"Please choose {alarmtype}", halign="center", font_size=24, color=[1,0,0,9])
        self.Box1.add_widget(self.Imagepop)
        self.Box1.add_widget(self.Labelpop)

        self.PopupPressed = Popup(title="Warning",
                                  separator_color=[1, 1, 1, 1],
                                  content=self.Box1,
                                  size_hint=(None, None),
                                  size=(450, 450),
                                  pos_hint={"center_x": .5, "center_y": .5},
                                  background="",
                                  auto_dismiss=True)
        self.PopupPressed.open()

    def Popup_info(self):
        Box=BoxLayout(orientation="vertical")
        label1=Label(text="",size_hint=(1,.1))
        Imagepo=Image(source="Pics/logorunistica.png",size_hint=(.7,.35),pos_hint={"center_x":.5,"center_y":.2})
        message= Label(text="Hier komt alle tekst over de app voor de gebruiker."
                            "Hier komt alle tekst over de app voor de gebruiker."
                            "Hier komt alle tekst over de app voor de gebruiker."
                            "Hier komt alle tekst over de app voor de gebruiker."
                            "Hier komt alle tekst over de app voor de gebruiker."
                            ,color=(0,0,0,1),font_size=16, text_size=(380, None),halign ="center",valign="center", size_hint=(1,.65))
        #Box.add_widget(label1)
        Box.add_widget(Imagepo)
        Box.add_widget(message)
        self.PopupPress = Popup(title="",
                                  separator_color=[0, 1, 0, 0],
                                  content= Box,
                                  size_hint=(None, None),
                                  size=(self.width-150,550),
                                  pos_hint={"center_x": .5, "center_y": .50},
                                  background="",
                                  auto_dismiss=True)

        self.PopupPress.open()

    def Popup_infomaster(self):
        Box = BoxLayout(orientation="vertical")
        label1 = Label(text="", size_hint=(1, .1))
        Imagepo = Image(source="Pics/logorunistica.png", size_hint=(.5, .25), pos_hint={"center_x": .5})

        message= Label(text="You can achieve the title 'Master in Runes' by getting good test results. The requirements to become a 'Master' are the following:\n\n(1) The minimum number of tests per category must be at least three.\n\n(2) Performance on each test-category will be an average of multiple tests results.\n\n(3) Your average overall test performance has to be at least 90%.\n\n" \
                      "(4) Test results per category will be weighted for the overall performance. The test regarding 'meaning of runes' will account for 50% of the overall score. The other tests, recognizing symbols en names of runes, will contribute each 25% respectively.\n\n Note: Learning Futhark runes for optimal tests results can easily be done via the 'Runes Academy' of Runistica. See option menu.",
                        color = (0, 0, 0, .75), halign = "left", valign = "center", font_size = 18, text_size = (450, None))
        Box.add_widget(Imagepo)
        Box.add_widget(message)

        self.Popuppie = Popup(title="",
                                  separator_color=[0, 1, 0, 0],
                                  #content= Label(text=f"{self.message}",color=(0,0,0,.75),halign="left", valign="center",font_size=16, text_size=(450, None)),
                                  content=Box,
                                  size_hint=(None, None),
                                  size=(self.width-150,900),
                                  pos_hint={"center_x": .5, "center_y": .5},
                                  background="",
                                  auto_dismiss=True)
        self.Popuppie.open()

    def Popup_delete_options(self, delete_buttons):

        self.Popuppie_buttons = Popup(title="Deleting test scores",
                                  title_size=22,
                                  title_color=[0,0,0,1],
                                  separator_color=[0, 0, 0, 1],
                                  content= delete_buttons,
                                  size_hint=(None, None),
                                  size=(450,575),
                                  pos_hint={"center_x": .5, "center_y": .5},
                                  background="",
                                  auto_dismiss=True)
        self.Popuppie_buttons.open()

class MainApp(App):

    def build(self):
        # 256 x 256 pixels
        #self.icon = "icon2.png"
        return RunenMasterScreens()

if __name__ == '__main__':
    MainApp().run()



