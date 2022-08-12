import random
import sqlite3

from kivy.uix.screenmanager import Screen,WipeTransition
from kivy.properties import StringProperty, ListProperty,NumericProperty

class MenuScreen(Screen):

	Trainingskeuze = StringProperty("")
	Antwoord_runen = ListProperty([])
	Quizz_runen= ListProperty([])
	antwoordcat = ListProperty([])
	quizz= ListProperty([])
	a_waarde = NumericProperty()
	teller = NumericProperty()
	Missed_quistions=ListProperty([])
	Score_quizz = NumericProperty(0)

	def quizzfunctie(self, quizztype, *args):

		if quizztype == "Runesymbols":
			a_waarde = 0

		elif quizztype == "SymbolNames":
			a_waarde = 1

		elif quizztype == "MeaningRunes":
			a_waarde = 2

		self.quizzbouw(a_waarde)

	def quizzbouw(self,a_waarde):

		conn = sqlite3.connect("dataRunistica.db")
		c = conn.cursor()
		c.execute("SELECT RuneNaam,RuneCredo, RuneText, Signtype FROM Runistica")
		datarune = c.fetchall()
		conn.commit()
		conn.close()

		rune_set = []
		for teken in datarune:
			rune_set.append(teken)
		random.shuffle(rune_set)

		# selecteer x runen-quizzvragen uit de database
		##############################################
		#################################################
		quizzduur = 10
		###################################################
		################################################

		rounds = 0
		runequizz = []
		for i in rune_set:
			if rounds < quizzduur:
			#voeg enkele eerste string van i toe (dus niet een mogelijke "V" string)
			#zolang deze rune nog niet opgenomen is in de set
				runequizz.append(i[0])
				rounds += 1

		# selecteer enkel de runenamen uit de gehele database
		rune_set1 = []
		for i in rune_set:
			rune_set1.append(i[0])

		# vorm een restant van niet gekozen runen (ontdubbelen shuffel ze ook)
		rune_rest = [rune for rune in rune_set1 if
					 rune not in runequizz]
		random.shuffle(rune_rest)
		self.Antwoord_runen = rune_rest
		self.Quizz_runen = runequizz

		self.quizz = []
		for i in runequizz:
			conn = sqlite3.connect("dataRunistica.db")
			c = conn.cursor()
			c.execute("SELECT RuneCredo FROM Runistica WHERE RuneNaam=(?)", (i,))
			datarune_quizzCredo = c.fetchone()
			self.quizz.append(datarune_quizzCredo)
			conn.commit()
			conn.close()

		#print(self.quizz)
		self.antwoordcat = []
		for i in rune_rest:
			conn = sqlite3.connect("dataRunistica.db")
			c = conn.cursor()
			c.execute("SELECT RuneCredo FROM Runistica WHERE RuneNaam=(?)", (i,))
			datarune_Credo = c.fetchone()
			self.antwoordcat.append(datarune_Credo)
			conn.commit()
			conn.close()
		#print(self.antwoordcat)

		self.quizz_meaning = []
		for i in runequizz:
			conn = sqlite3.connect("dataRunistica.db")
			c = conn.cursor()
			c.execute("SELECT RuneText FROM Runistica WHERE RuneNaam=(?)", (i,))
			datarune_quizzMeaning = c.fetchone()
			self.quizz_meaning.append(datarune_quizzMeaning)
			conn.commit()
			conn.close()
		#print(str(self.quizz_meaning))

		self.antwoordcat_meaning = []
		for i in rune_rest:
			conn = sqlite3.connect("dataRunistica.db")
			c = conn.cursor()
			c.execute("SELECT RuneText FROM Runistica WHERE RuneNaam=(?)", (i,))
			datarune_Meaning = c.fetchone()
			self.antwoordcat_meaning.append(datarune_Meaning[0])
			conn.commit()
			conn.close()
		#print(self.antwoordcat_meaning)

		#stuur naar volgende pagina alvast de eerste vraag (symbool & antwoorden)
		self.manager.screens[(int(3 + a_waarde))].ids._PictureChoice.source = "Tekens/" + runequizz[0] + ".png"

		if a_waarde == 0:

			self.manager.screens[(int(3 + a_waarde))].ids._antw1.text = self.Quizz_runen[0]
			self.manager.screens[(int(3 + a_waarde))].ids._antw2.text = self.Antwoord_runen[1]
			self.manager.screens[(int(3 + a_waarde))].ids._antw3.text = self.Antwoord_runen[2]
			self.manager.screens[(int(3 + a_waarde))].ids._antw4.text = self.Antwoord_runen[3]
		elif a_waarde == 1:
			self.manager.screens[(int(3 + a_waarde))].ids._antw1.text = self.quizz[0][0]
			self.manager.screens[(int(3 + a_waarde))].ids._antw2.text = self.antwoordcat[1][0]
			self.manager.screens[(int(3 + a_waarde))].ids._antw3.text = self.antwoordcat[2][0]
			self.manager.screens[(int(3 + a_waarde))].ids._antw4.text = self.antwoordcat[3][0]

		elif a_waarde == 2:
			self.manager.screens[(int(3 + a_waarde))].ids._antw1.text = self.quizz_meaning[0][0]
			self.manager.screens[(int(3 + a_waarde))].ids._antw2.text = self.antwoordcat_meaning[1]
			self.manager.screens[(int(3 + a_waarde))].ids._antw3.text = self.antwoordcat_meaning[2]
			self.manager.screens[(int(3 + a_waarde))].ids._antw4.text = self.antwoordcat_meaning[3]


	def transport(self):

		if self.Trainingskeuze == "Runesymbols":
		#	print("symbols gekozen")

			# creeer alvast de quizzvragen
			self.quizzfunctie("Runesymbols")
			# ga naar volgend scherm
			self.ids._Symbols_but.active = False
			# reset de tellers
			self.Trainingskeuze = ""
			self.ids._ButtonStart.text = "Choose\n Training/ College"

			# extreem belangrijk self.teller= 0 werkt nml niet!!!!!!
			self.a_waarde = 0
			self.manager.screens[3].Score_quizz = 0
			self.manager.screens[3].teller = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[4].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []

			self.manager.current = "vragenscreen"
			self.manager.transition = WipeTransition(duration=1)
			#self.manager.transition.direction = "right"

		elif self.Trainingskeuze == "SymbolNames":

			self.quizzfunctie("SymbolNames")
			self.ids._Names_but.active=False
			# reset tellers
			self.Trainingskeuze = ""
			self.ids._ButtonStart.text = "Choose\n Training/ College"
			self.a_waarde = 0
			# extreem belangrijk self.teller= 0 werkt nml niet!!!!!!
			self.manager.screens[4].Score_quizz = 0
			self.manager.screens[4].teller = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []
			self.manager.current = "vragenscreen1"
			self.manager.transition =  WipeTransition(duration=1)
		#	print("Names gekozen")

		elif self.Trainingskeuze == "Meaning of Runes":

			self.quizzfunctie("MeaningRunes")
			self.ids._Meaning_but.active = False

			# reset tellers
			self.Trainingskeuze = ""
			self.ids._ButtonStart.text = "Choose\n Training/ College"
			self.a_waarde = 0

			# extreem belangrijk self.teller= 0 werkt nml niet!!!!!!
			self.manager.screens[5].teller = 0
			self.manager.screens[5].Score_quizz = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[4].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []
			# ga naar antwoorden-scherm
			self.manager.current = "vragenscreen2"
			self.manager.transition = WipeTransition(duration=1)
		#	print("Meaning gekozen")

		elif self.Trainingskeuze == "College Symbols":

			self.ids._Symbols_college.active = False
			# reset tellers
			self.Trainingskeuze = ""
			self.ids._ButtonStart.text = "Choose\n Training/ College"

			# bij eerder gespeelde kwis alle resultaten wissen
			self.manager.screens[5].teller = 0
			self.manager.screens[5].Score_quizz = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[4].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []
			# ga naar college symbols-scherm
			self.manager.current = "CollegeSymbols_screen"
			self.manager.transition = WipeTransition(duration=1)
		#	print("College Symbols gekozen")

		elif self.Trainingskeuze == "College Names":

			self.ids._Names_college.active = False
			# reset tellers
			self.Trainingskeuze = ""
			self.ids._ButtonStart.text = "Choose\n Training/ College"

			# bij eerder gespeelde kwis alle resultaten wissen
			self.manager.screens[5].teller = 0
			self.manager.screens[5].Score_quizz = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[4].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []
			# ga naar college symbols-scherm
			self.manager.current = "CollegeNames_screen"
			self.manager.transition = WipeTransition(duration=1)
		#	print("College Names gekozen")


		elif self.Trainingskeuze == "":
			self.manager.Popup_Choose("a module to train")