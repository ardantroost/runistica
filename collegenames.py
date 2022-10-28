import sqlite3
from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty,Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import random


class CollegeNamesScreen(Screen):

	score_symbol = NumericProperty(0)
	score_naam = NumericProperty(0)
	score_meaning = NumericProperty(0)
	tries = NumericProperty(0)
	deltaNaam= NumericProperty(0)
	deltaSymbol= NumericProperty(0)
	deltaMeaning= NumericProperty(0)

	datarune= ListProperty([])

	def on_leave(self):

		self.score_symbol = 0
		self.score_naam = 0
		self.score_meaning = 0
		self.tries = 0
		self.deltaNaam =0
		self.deltaSymbol = 0
		self.deltaMeaning = 0

		self.clear_carousels()
		#clear statistics
		self.ids._symbol_score.text = ""
		self.ids._naam_score.text = ""
		self.ids._meaning_score.text = ""
		self.ids._pie_perf.level = 0
		self.ids._Buttoncheck.text = "Check"

	def on_enter(self, *args):

		conn = sqlite3.connect("dataRunistica.db")
		c = conn.cursor()
		c.execute("SELECT RuneNaam,RuneCredo,RuneText,Signtype FROM Runistica")
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

			rune_association = rune[1]
			Labelx= Label(text=rune_association, font_size=18)
			self.ids._Carou2.add_widget(Labelx)
			self.ids._Carou2.index = random.choice(range(1,28))
			self.ids._Carou2.color = [0, 0, 0, 1]
			self.ids._Carou2_result.text=""

			rune_symbol = rune[0]
			Labely = Label(text=rune_symbol, font_size=18)
			self.ids._Carou1a.add_widget(Labely)
			self.ids._Carou1a.index = random.choice(range(1, 28))
			self.ids._Carou1a.color = [0, 0, 0, 1]
			self.ids._Carou1a_result.text = ""

			rune_meaning = rune[2]
			Labelz = Label(text=rune_meaning, text_size=(140,None))
			self.ids._Carou1b.add_widget(Labelz)
			self.ids._Carou1b.index = random.choice(range(1, 28))
			self.ids._Carou1b.color = [0, 0, 0, 1]
			self.ids._Carou1b_result.text = ""

		return self.datarune
	def clear_carousels(self,*args, **kwargs):

		# leeg al de carousels
		self.ids._Carou1.clear_widgets(children=None, *args, **kwargs)
		self.ids._Carou1b.clear_widgets(children=None, *args, **kwargs)
		self.ids._Carou1a.clear_widgets(children=None, *args, **kwargs)
		self.ids._Carou2.clear_widgets(children=None, *args, **kwargs)

	def newcombination(self,*args,**kwargs):

		#leeg caroucels
		self.clear_carousels()
		# vul alle carousels met nieuwe vraag
		self.on_enter()
		# muteer button om de geswipte antwoorden te kunnen checken
		self.ids._Buttoncheck.text = "Check"

	def anim_answer_incorrect(self,widget):

		anim = Animation(color = [1,1,1,1], duration= 1)
		anim.start(widget)

	def anim_answer_correct(self,widget):

		anim = Animation(color = [0,0,0,0], duration= 1)
		anim.start(widget)

	def Checkcombination(self, slidervalue, *args):

		self.juiste_symbol = self.datarune[slidervalue][1]
		self.juiste_naam = self.datarune[slidervalue][0]
		self.juiste_meaning = self.datarune[slidervalue][2]

		self.check_symbol = self.ids._Carou2.current_slide.text
		self.check_naam = self.ids._Carou1a.current_slide.text
		self.check_meaning = self.ids._Carou1b.current_slide.text

		self.tries += 1

		# symbolcontrole
		if self.juiste_symbol == self.check_symbol:
			self.ids._Carou2_result.text = "Correct"
			self.ids._Carou2.current_slide.color = [0, 1, 0, 1]
			Clock.schedule_once(lambda a: self.anim_answer_correct(self.ids._Carou2_result),2)
			self.score_naam+= 1
			self.deltaNaam+=1

		else:
			self.ids._Carou2_result.text = "Incorrect:\n"+self.juiste_symbol
			self.ids._Carou2.current_slide.color = [1, 0, 0, 1]
			Clock.schedule_once(lambda a: self.anim_answer_incorrect(self.ids._Carou2_result), 2)

		# naamcontrole
		if self.juiste_naam == self.check_naam:
			self.ids._Carou1a.current_slide.color= [0,1,0,1]
			self.ids._Carou1a_result.text = "Correct"
			Clock.schedule_once(lambda a: self.anim_answer_correct(self.ids._Carou1a_result), 2)
			self.score_symbol += 1
			self.deltaSymbol += 1

		else:
			self.ids._Carou1a.current_slide.color = [1, 0, 0, 1]
			self.ids._Carou1a_result.text = "Incorrect:\n"+self.juiste_naam
			Clock.schedule_once(lambda a: self.anim_answer_incorrect(self.ids._Carou1a_result), 2)

		# meaningcontrole
		if self.juiste_meaning == self.check_meaning:
			self.ids._Carou1b.current_slide.color = [0, 1, 0, 1]
			self.ids._Carou1b_result.text = "Correct"
			Clock.schedule_once(lambda a: self.anim_answer_correct(self.ids._Carou1b_result), 2)
			self.score_meaning += 1
			self.deltaMeaning += 1

		else:
			self.ids._Carou1b.current_slide.color = [1, 0, 0, 1]
			self.ids._Carou1b_result.text = "Incorrect:\n"+self.juiste_meaning
			Clock.schedule_once(lambda a: self.anim_answer_incorrect(self.ids._Carou1b_result), 2)

		self.a_perf= (self.score_symbol/self.tries)
		self.b_perf= (self.score_naam)/ (self.tries)
		self.c_perf= (self.score_meaning)/ (self.tries)
		self.perf=(self.a_perf+self.b_perf+self.c_perf)/3

		self.ids._symbol_score.text = str(format(self.a_perf*100,".1f")+"%")
		self.ids._naam_score.text = str(format(self.b_perf*100,".1f")+"%")
		self.ids._meaning_score.text = str(format(self.c_perf*100,".1f")+"%")

		#self.ids._pie_perf.level = format(self.perf,"1f")
		self.ids._pie_perf.level = (self.perf*360)
		self.balance=(self.deltaMeaning + self.deltaNaam + self.deltaSymbol)

		if self.balance == 3:
			self.full_strike()
		else:
			pass

		self.deltaMeaning=0
		self.deltaNaam=0
		self.deltaSymbol=0
		self.balance=0

		# verander buttton voor selectie nieuwe combinatie
		self.ids._Buttoncheck.text = "New\nRune"

	def full_strike(self):
		self.manager.Popup_Practicum()







