import sqlite3

from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty,Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import random


class CollegeNamesScreen(Screen):

	score = NumericProperty(0)
	tries = NumericProperty(0)

	datarune= ListProperty([])

	def on_leave(self):
		self.score = 0
		self.tries = 0
		self.ids._score.text = " "

	def on_enter(self, *args):

		conn = sqlite3.connect("dataRunistica.db")
		c = conn.cursor()
		c.execute("SELECT RuneNaam,RuneCredo,Signtype FROM Runistica")
		self.datarune = c.fetchall()
		random.shuffle(self.datarune)
		conn.commit()
		conn.close()

		for rune in self.datarune:

			a = "".join([str(rune[0][:1]).lower(),str((rune[0][1:]).lower())])
			Imagex = Image(source= "Tekens/" +a+ ".png",width=150,height=150,keep_ratio=False,allow_stretch=True,
						   size_hint=(None,None), pos_hint={"center_x":.5,"center_y":.5})
			self.ids._Carou1.add_widget(Imagex)
			self.ids._Carou1.index = random.choice(range(1,28))

			b = rune[1]
			Labelx= Label(text=b)
			self.ids._Carou2.add_widget(Labelx)
			self.ids._Carou2.index = random.choice(range(1,28))

		return self.datarune

	def anim_answer(self,widget):
		anim = Animation(color = [1,0,1,0], duration= .1)
		anim.start(widget)

	def Checkcombination(self, slidervalue, *args):

		#b=(((self.ids._Carou1.current_slide.source).replace(".png", "")).replace("Tekens/", "")).capitalize()

		check2 = self.datarune[slidervalue][1]
		check3 = self.ids._Carou2.current_slide.text

		if check2 == check3:

			self.ids._result1.text="Your answer is: correct"
			self.ids._result1.color = [0, 1, 0, 1]
			Clock.schedule_once(lambda a: self.anim_answer(self.ids._result1),2)
			self.score+= 1
			self.tries += 1
			self.ids._score.text = "Score: " + str(self.score) + "\\" + str(self.tries)

		else:
			self.ids._result1.text = "Your answer is: not yet correct"
			self.ids._result1.color = [1,0,0,1]
			Clock.schedule_once(lambda a:self.anim_answer(self.ids._result1), 2)
			self.tries += 1
			self.ids._score.text= "Score: "+str(self.score) + "\\" + str(self.tries)






