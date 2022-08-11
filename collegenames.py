import sqlite3
from kivy.properties import ListProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import random



class CollegeNamesScreen(Screen):


	datarune= ListProperty([])


	def on_enter(self, *args):

		conn = sqlite3.connect("dataRunistica.db")
		c = conn.cursor()
		c.execute("SELECT RuneNaam,RuneCredo,Signtype FROM Runistica")
		self.datarune = c.fetchall()
		conn.commit()
		conn.close()

		for rune in self.datarune:

			a= ''.join([str(rune[0][:1]).lower(),str((rune[0][1:]))])
			Imagex=Image(source= "Tekens/"+a+ ".png")
			self.ids._Carou1.add_widget(Imagex)
			self.ids._Carou1.index = random.choice(range(1,28))

			b = rune[1]
			Labelx=Label(text=b)
			self.ids._Carou2.add_widget(Labelx)
			self.ids._Carou2.index=random.choice(range(1,18))

		return self.datarune

	def Checkcombination(self, slidervalue, *args):

		conn = sqlite3.connect("dataRunistica.db")
		c = conn.cursor()
		c.execute("SELECT RuneNaam,RuneCredo,Signtype FROM Runistica")
		self.datarune = c.fetchall()
		conn.commit()
		conn.close()

		#print((self.ids._Carou2.current_slide.text))
		b=(((self.ids._Carou1.current_slide.source).replace(".png", "")).replace("Tekens/", "")).capitalize()
		#print(b)

		self.ids._result2.text = b
		self.ids._result2.color = 0,1,0,1

		check1 = self.datarune[slidervalue][0]
		check2 = self.datarune[slidervalue][1]
		check3 = self.ids._Carou2.current_slide.text

		if check2== check3:
			self.ids._result1.text="Uw antwoord is:"
			self.ids._result2.text = "Juist "

		else:
			self.ids._result1.text = "Uw antwoord is:"
			self.ids._result2.text = "Niet juist "





