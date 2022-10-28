import random
import sqlite3
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty


class CollegeSymbolsScreen(Screen):

	list_runen = ListProperty([])

	def stripper(self, value):

		if value == "next_slide":

			text1 = self.ids._CarouselSelf.next_slide.source

		else:
			text1 = self.ids._CarouselSelf.previous_slide.source

		text1=text1.replace('.png','')
		text1=text1.replace("Tekens/","")

		self.ids._naam.text = text1.capitalize()

		text1 = text1.capitalize()
		text1 = text1.replace(" v", " V")

		conn = sqlite3.connect("dataRunistica.db")
		c = conn.cursor()
		c.execute("SELECT RuneCredo, RuneText FROM Runistica WHERE RuneNaam =(?)", (str(text1),))
		datae = c.fetchall()
		conn.commit()
		conn.close()

		self.ids._symbol.text = str(datae[0][0])
		self.ids._meaning.text = str(datae[0][1])
		if text1[-1]== "v" or text1[-1]== "V":
			self.ids._reverse.text = "<reversed rune>"
		else:
			self.ids._reverse.text = ""



	# automatische start van methode bij open van dit scherm (on_start werkt niet!!!!)
	def on_enter(self):

		conn = sqlite3.connect("dataRunistica.db")
		c = conn.cursor()
		c.execute("SELECT RuneNaam,RuneCredo, RuneText, Signtype FROM Runistica")
		datarune = c.fetchall()
		random.shuffle(datarune)
		conn.commit()
		conn.close()

		self.carouselShow = self.ids._CarouselSelf

		for i in datarune:

			src = "Tekens/"+ i[0].lower() +".png"
			image  = Image(source= src, width=150,height=150,keep_ratio=False,allow_stretch=True, size_hint=(None,None), pos_hint={"center_x":.5,"center_y":.5} )
			label  = Label(text=i[0], font_size=24,color=(1, 1, 1, 1),halign= "left", valign="center")
			label.text.replace(".png","")
			label.text.replace("Tekens/","")
			
			self.carouselShow.add_widget(image)

		self.ids._naam.text = str(datarune[0][0])
		self.ids._symbol.text = str(datarune[0][1])
		self.ids._meaning.text = str(datarune[0][2])

		if datarune[0][0][-1]== "v" or datarune[0][0][-1]== "V":
			self.ids._reverse.text = "<reversed rune>"
		else:
			self.ids._reverse.text = ""




