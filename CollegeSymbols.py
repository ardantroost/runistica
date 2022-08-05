import sqlite3

from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import Screen, RiseInTransition,FallOutTransition, WipeTransition
from kivy.core.window import Window
import random
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.animation import Animation


class CollegeSymbolsScreen(Screen):

	list_runen=ListProperty([])

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

		self.ids._symbol.text = "Symbol: "+ str(datae[0][0])
		self.ids._meaning.text = "Message: \n" + str(datae[0][1])

	# automatische start van methode bij open van dit scherm (on_start werkt niet!!!!)
	def on_enter(self):
		conn = sqlite3.connect("dataRunistica.db")
		c = conn.cursor()
		c.execute("SELECT RuneNaam,RuneCredo, RuneText, Signtype FROM Runistica")
		datarune = c.fetchall()
		conn.commit()
		conn.close()

		self.carouselShow = self.ids._CarouselSelf

		for i in datarune:

			src = "Tekens/"+ i[0].lower() +".png"
			image  = Image(source= src)
			label  = Label(text=i[0], font_size=24,color=(1, 1, 1, 1),halign= "left", valign="center")
			label.text.replace(".png","")
			label.text.replace("Tekens/","")
			
			self.carouselShow.add_widget(image)

		self.ids._naam.text = str(datarune[0][0])
		self.ids._symbol.text = str(datarune[0][1])
		self.ids._meaning.text = str(datarune[0][2])


