import random
import sqlite3
import time

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.animation import Animation

class VragenScreeneen(Screen):

	PictureChoice = StringProperty("")
	answerquizz = StringProperty("")
	Score_quizz = NumericProperty(0)
	Symbol_check = StringProperty("")
	Missed_quistions = ListProperty([])
	Missed_runes = ListProperty([])
	teller=NumericProperty(0)

	def on_enter(self, *args):

		self.Symbol_start= self.manager.get_screen("menuscreen").Quizz_runen
		self.ids._PictureChoice.source = "Tekens/" + self.Symbol_start[0].lower() + ".png"

		# start Quizz-timer
		self.starttime=time.time()

	def scorevertaler(self):

		self.lanquage = self.manager.lanquage
		conn = sqlite3.connect("taalkeuze.db")
		c = conn.cursor()

		if self.lanquage == 'Engels':
			c.execute("SELECT namestext,text2,text3,text4,text5,text6 FROM score WHERE taal=(?)", ("Engels",))
			scoretexten = c.fetchall()
		elif self.lanquage == 'Frans':
			c.execute("SELECT namestext,text2,text3,text4,text5,text6 FROM score WHERE taal=(?)", ("Frans",))
			scoretexten = c.fetchall()
		elif self.lanquage == 'Duits':
			c.execute("SELECT namestext,text2,text3,text4,text5,text6 FROM score WHERE taal=(?)", ("Duits",))
			scoretexten = c.fetchall()
		elif self.lanquage == 'Nederlands':
			c.execute("SELECT namestext,text2,text3,text4,text5,text6 FROM score WHERE taal=(?)", ("Nederlands",))
			scoretexten = c.fetchall()

		conn.commit()
		conn.close()

		self.scoretexten = scoretexten


	def on_leave(self, *args):
		self.saveresults("Names")

	def saveresults(self, Testtype):

		conn = sqlite3.connect("dataRunistica.db")
		c = conn.cursor()
		for elke in self.Missed_quistions:
			c.execute("SELECT RuneNaam FROM Runistica WHERE RuneCredo=(?)",(elke,))
			i = c.fetchone()
			self.Missed_runes.append(i[0])
		conn.commit()
		conn.close()

		conn = sqlite3.connect("masterresults.db")
		c2 = conn.cursor()
		for Rune in self.Missed_runes:
			c2.execute("INSERT INTO Advice VALUES (?,?)", (Rune,Testtype))
		conn.commit()
		conn.close()

	def updatedatabase(self,score_quizz, Symboltraining, Symbolscore, Nametraining, Meaningtraining,Meaningscore,Time):

		Lastvisit = time.strftime("%d-%m-%Y")
		Visittime = time.strftime("%X")
		Namescore = score_quizz


		conn = sqlite3.connect("masterresults.db")
		c = conn.cursor()
		c.execute("INSERT INTO masterresults VALUES (?,?,?,?,?,?,?,?,?)" ,
				  (Lastvisit, Visittime, Symboltraining, Symbolscore, Nametraining, Namescore, Meaningtraining,Meaningscore,Time) )
		conn.commit()
		conn.close()

	def Score (self):

		self.Symbol_check= self.manager.get_screen("menuscreen").quizz[self.teller][0]
		if self.answerquizz == self.Symbol_check:
			self.Score_quizz +=1
		else:
			self.Missed_quistions.append(self.Symbol_check)

	def ConstructQuizz(self, waarde):

			# importeer de 2 lijsten met de quizzvragen en de antwoorden
			Antwoord_runen = self.manager.get_screen("menuscreen").antwoordcat
			Quizz_runen = self.manager.get_screen("menuscreen").Quizz_runen
			quizz= self.manager.get_screen("menuscreen").quizz

			self.teller += waarde
			Einde_vragen = int(len(Quizz_runen))

			if self.teller < Einde_vragen:

				# pick het volgende symbool uit de selectiegroep met vragen
				self.Symbol = "Tekens/" + Quizz_runen[self.teller].lower() + ".png"

				# prepareer antwoordmogelijkheden incl het juiste antwoord
				self.multiplechoice_set = random.sample(Antwoord_runen, 3)
				# voeg juiste antwoord toe
				self.multiplechoice_set.append(quizz[self.teller])
				random.shuffle(self.multiplechoice_set)

				# print symbool en antwoorden op "screen"
				self.ids._PictureChoice.source = self.Symbol
				# start animatie RuneTeken
				self.Anim(self.ids._PictureChoice)
				# start animatie vraagstelling
				self.Anim1(self.ids._label_vraag)

				self.ids._antw1.text = self.multiplechoice_set[0][0]
				self.ids._antw2.text = self.multiplechoice_set[1][0]
				self.ids._antw3.text = self.multiplechoice_set[2][0]
				self.ids._antw4.text = self.multiplechoice_set[3][0]

				# leegmaken van antwoord (voor call bij niet antwoorden)
				self.answerquizz = ''

			# als alle vragen gesteld zijn score en leersymbolen laten zien
			else:
				# bereidt vertaling voor van de testuitslag
				self.scorevertaler()

				if len(self.Missed_quistions) > 0:

					#self.print = (f"End of training the association of runes!,\n {self.Score_quizz} out of 10 "
					#			  f"is your testscore.\n For more insight which symbols\n are in need of practice\n press Button")

					self.print = str(self.scoretexten[0][0]) + str(self.Score_quizz) + " " + str(self.scoretexten[0][1]) + " " + str(self.scoretexten[0][2])

					self.manager.screens[6].ids._ResultNaam.text = self.print
					self.manager.screens[6].ids._ButtonAdvice.text = str(self.scoretexten[0][4])
					self.manager.current = "resultscreen"

				else:
					#self.print = (f"End of training the association of runes!,\n {self.Score_quizz} is your endscore\n "
					#			  f"This is 100%\n "
					#			  f"None of the runes are incorrectly answered.\n "
					#			  f"Well done You!")

					self.print = str(self.scoretexten[0][0]) + str(self.Score_quizz) + " " + str(self.scoretexten[0][3])
					self.manager.screens[6].ids._ResultNaam.text = self.print

					#self.manager.screens[6].ids._ButtonAdvice.text = "<< End >>"
					self.manager.screens[6].ids._ButtonAdvice.text = str(self.scoretexten[0][5])
					self.manager.current = "resultscreen"

				# stop Quizz-timer, bereken tijdsduur en transporteer deze met andere gegevens
				self.endtime = time.time()
				self.deltatime_name = self.endtime - self.starttime
				self.updatedatabase(self.Score_quizz, Symboltraining=0, Symbolscore=0,Nametraining=1,Meaningtraining=0,Meaningscore=0,Time=format(self.deltatime_name,'.1f'))

	# animatie van geprinte RuneTeken
	def Anim1(self, widget,*args):
		anim= Animation(color=[1,1,1,0],duration=.5)
		anim += Animation(color=[1,1,1,1],duration=.5, bold=True)
		anim.start(widget)

	def Anim(self, widget,*args):
		anim = Animation(width=0,height=0, duration=.5)
		anim += Animation(duration=.5, width=100,height=100)
		anim.start(widget)

	def ClearButtons(self):
		self.ids._antw1.background_color = [1,1,1,0]
		self.ids._antw2.background_color = [1,1,1,0]
		self.ids._antw3.background_color = [1,1,1,0]
		self.ids._antw4.background_color = [1,1,1,0]

	def PressedButton(self, answer):

			if answer == self.ids._antw1.text:
				self.answerquizz = self.ids._antw1.text
			elif answer == self.ids._antw2.text:
				self.answerquizz = self.ids._antw2.text
			elif answer == self.ids._antw3.text:
				self.answerquizz = self.ids._antw3.text
			elif answer == self.ids._antw4.text:
				self.answerquizz = self.ids._antw4.text

	def SubmittAnswer(self) :
		# als er een antwoord gekozen is:
		if len(self.answerquizz)>0:
			self.Score()
			self.ConstructQuizz(1)

		# als antwoord nog NIET gekozen is
		else:
			self.manager.Popup_Choose("an answer")