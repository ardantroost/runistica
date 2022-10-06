import random
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.animation import Animation

class VragenScreen2(Screen):

	PictureChoice = StringProperty("")
	answerquizz = StringProperty("")
	Score_quizz = NumericProperty(0)
	Symbol_check = StringProperty("")
	Missed_quistions = ListProperty([])
	teller=NumericProperty()

	def CleanUp(self, *args):

		self.teller= 0
		self.Missed_quistions = []
		self.Score_quizz = 0

	def Score (self):

		self.Symbol_check = self.manager.get_screen("menuscreen").quizz_meaning[self.teller][0]
		if self.answerquizz == self.Symbol_check:
			self.Score_quizz +=1
		else:
			self.Missed_quistions.append(self.Symbol_check)

	def ConstructQuizz(self, waarde):

			# importeer de 2 lijsten met de quizzvragen en de antwoorden
			Antwoord_runen = self.manager.get_screen("menuscreen").antwoordcat_meaning
			Quizz_runen = self.manager.get_screen("menuscreen").Quizz_runen
			Quizz_runen_meaning= self.manager.get_screen("menuscreen").quizz_meaning

			self.teller += waarde
			Einde_vragen = int(len(Quizz_runen))

			if self.teller < Einde_vragen:

				# pick het volgende symbool uit de selectiegroep met vragen
				self.Symbol = "Tekens/" + Quizz_runen[self.teller].lower() + ".png"

				# prepareer antwoordmogelijkheden incl het juiste antwoord
				self.multiplechoice_set = random.sample(Antwoord_runen, 3)
				self.multiplechoice_set.append(Quizz_runen_meaning[self.teller][0])
				random.shuffle(self.multiplechoice_set)

				# print symbool en antwoorden op "screen"
				self.ids._PictureChoice.source = self.Symbol
				# start animatie RuneTeken
				self.Anim(self.ids._PictureChoice)
				# start animatie vraagstelling
				self.Anim1(self.ids._Vraag_label)

				self.ids._antw1.text = self.multiplechoice_set[0]
				self.ids._antw2.text = self.multiplechoice_set[1]
				self.ids._antw3.text = self.multiplechoice_set[2]
				self.ids._antw4.text = self.multiplechoice_set[3]

				# leegmaken van gegeven antwoord (voor call bij niet antwoorden)
				self.answerquizz = ''

			# als alle vragen gesteld zijn score en leersymbolen laten zien in ander scherm RESULT
			else:
				if len(self.Missed_quistions)> 0:
					self.print = (f"End of training the interpretation of runes!,\n {self.Score_quizz} out of 10 "
						  f" is your endscore\n"
						  f"Some symbols need to be studied a bit more:\n"
						f"Press button below for more information")

					self.manager.screens[6].ids._ResultNaam.text = self.print
					self.manager.current = "resultscreen"

				else:
					self.print= (f"End of training the interpretation of runes!, {self.Score_quizz} "
						  f"is your endscore\n This a 100% score"
						  f"None of these runes are unclear to you. Well done")

					self.manager.screens[6].ids._ResultNaam.text = self.print
					self.manager.screens[6].ids._ButtonAdvice.text = "<< Training advice >>"
					self.manager.current = "resultscreen"

	# animatie van geprinte RuneTeken
	def Anim1(self, widget,*args):
		anim= Animation(color=[1,1,1,0],duration=.5)
		anim += Animation(color=[1,1,1,1],duration=.5, bold=True)
		anim.start(widget)

	def Anim(self, widget,*args):
		anim = Animation(size_hint=(1, 0), duration=.5)
		anim += Animation(duration=.5, size_hint=(1, 1))
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

		# als antwoord nog gekozen is
		if len(self.answerquizz)>0:
			self.Score()
			self.ConstructQuizz(1)

		# als antwoord nog NIET gekozen is met de Button waarschuwing (RUNENMASTER.py)
		else:
			self.manager.Popup_Choose("an answer")