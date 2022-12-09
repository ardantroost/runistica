import random
import sqlite3
from kivy.uix.screenmanager import Screen,WipeTransition
from kivy.properties import StringProperty, ListProperty,NumericProperty

class MenuScreen(Screen):

	def on_enter(self, *args):
		self.lanquage = self.manager.lanquage


	Trainingskeuze = StringProperty("")
	Antwoord_runen = ListProperty([])
	Quizz_runen= ListProperty([])
	runequizz = ListProperty([])
	antwoordcat = ListProperty([])
	quizz= ListProperty([])
	a_waarde = NumericProperty()
	teller = NumericProperty()
	Missed_quistions = ListProperty([])
	Missed_runes = ListProperty([])
	Score_quizz = NumericProperty(0)

	def textinfo(self):

		self.manager.Popup_info()


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
		quizzduur = 2
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

		# vorm een restant van niet gekozen runen (ontdubbel en shuffel ze ook)
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

		self.antwoordcat = []
		for i in rune_rest:
			conn = sqlite3.connect("dataRunistica.db")
			c = conn.cursor()
			c.execute("SELECT RuneCredo FROM Runistica WHERE RuneNaam=(?)", (i,))
			datarune_Credo = c.fetchone()
			self.antwoordcat.append(datarune_Credo)
			conn.commit()
			conn.close()

		self.quizz_meaning = []
		for i in runequizz:
			conn = sqlite3.connect("dataRunistica.db")
			c = conn.cursor()
			c.execute("SELECT RuneText FROM Runistica WHERE RuneNaam=(?)", (i,))
			datarune_quizzMeaning = c.fetchone()
			self.quizz_meaning.append(datarune_quizzMeaning)
			conn.commit()
			conn.close()

		self.antwoordcat_meaning = []
		for i in rune_rest:
			conn = sqlite3.connect("dataRunistica.db")
			c = conn.cursor()
			c.execute("SELECT RuneText FROM Runistica WHERE RuneNaam=(?)", (i,))
			datarune_Meaning = c.fetchone()
			self.antwoordcat_meaning.append(datarune_Meaning[0])
			conn.commit()
			conn.close()

		#stuur naar volgende gekozen pagina alvast de eerste vraag (symbool & antwoorden)

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

	def knopvertaler(self):

		self.lanquage = self.manager.lanquage

		conn = sqlite3.connect("taalkeuze.db")
		c = conn.cursor()
		if self.lanquage == 'Engels':
			c.execute("SELECT choose_eng FROM menu")
			texten = c.fetchall()
		elif self.lanquage == 'Frans':
			c.execute("SELECT choose_fr FROM menu")
			texten = c.fetchall()
		elif self.lanquage == 'Duits':
			c.execute("SELECT choose_dts FROM menu")
			texten = c.fetchall()
		elif self.lanquage == 'Nederlands':
			c.execute("SELECT choose_ned FROM menu")
			texten = c.fetchall()

		conn.commit()
		conn.close()
		# voor transport....(elders gebruik)

		self.knoptext = texten

	def transport(self):

		self.knopvertaler()

		if self.Trainingskeuze == "Runesymbols":

			# creeer alvast de quizzvragen
			self.quizzfunctie("Runesymbols")
			# ga naar volgend scherm
			self.ids._Symbols_but.active = False

			# reset de tellers
			self.Trainingskeuze = ""
			##self.ids._ButtonStart.text = "Choose"
			self.ids._ButtonStart.text = str(self.knoptext[0][0])

			# extreem belangrijk self.teller= 0 werkt nml niet!!!!!!
			self.a_waarde = 0

			self.manager.screens[3].Score_quizz = 0
			self.manager.screens[3].teller = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[4].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []
			self.manager.screens[3].Missed_runes = []
			self.manager.screens[4].Missed_runes = []
			self.manager.screens[5].Missed_runes = []

			self.manager.current = "vragenscreen"
			self.manager.transition = WipeTransition(duration=1)

		elif self.Trainingskeuze == "SymbolNames":

			self.quizzfunctie("SymbolNames")
			self.ids._Names_but.active=False

			# reset tellers
			self.Trainingskeuze = ""
			##self.ids._ButtonStart.text = "Choose"
			self.ids._ButtonStart.text = str(self.knoptext[0][0])
			self.a_waarde = 0

			# extreem belangrijk self.teller= 0 werkt nml niet!!!!!!
			self.manager.screens[4].Score_quizz = 0
			self.manager.screens[4].teller = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[4].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []
			self.manager.screens[3].Missed_runes = []
			self.manager.screens[4].Missed_runes = []
			self.manager.screens[5].Missed_runes = []

			self.manager.current = "vragenscreeneen"
			self.manager.transition =  WipeTransition(duration=1)

		elif self.Trainingskeuze == "Meaning of Runes":

			self.quizzfunctie("MeaningRunes")
			self.ids._Meaning_but.active = False

			# reset tellers
			self.Trainingskeuze = ""
			#self.ids._ButtonStart.text = "Choose"
			self.ids._ButtonStart.text = str(self.knoptext[0][0])
			self.a_waarde = 0

			# extreem belangrijk self.teller= 0 werkt nml niet!!!!!!
			self.manager.screens[5].teller = 0
			self.manager.screens[5].Score_quizz = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[4].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []
			self.manager.screens[3].Missed_runes = []
			self.manager.screens[4].Missed_runes = []
			self.manager.screens[5].Missed_runes = []

			# ga naar antwoorden-scherm
			self.manager.current = "vragenscreentwee"
			self.manager.transition = WipeTransition(duration=1)


		elif self.Trainingskeuze == "College Symbols":

			self.ids._Symbols_college.active = False
			# reset tellers
			self.Trainingskeuze = ""
			#self.ids._ButtonStart.text = "Choose"
			self.ids._ButtonStart.text = str(self.knoptext[0][0])

			# bij eerder gespeelde kwis alle resultaten wissen
			self.manager.screens[5].teller = 0
			self.manager.screens[5].Score_quizz = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[4].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []

			# ga naar college symbols-scherm
			self.manager.current = "collegesymbolsscreen"
			self.manager.transition = WipeTransition(duration=1)

		elif self.Trainingskeuze == "College Names":

			self.ids._Names_college.active = False
			# reset tellers
			self.Trainingskeuze = ""
			#self.ids._ButtonStart.text = "Choose"
			self.ids._ButtonStart.text = str(self.knoptext[0][0])

			# bij eerder gespeelde kwis alle resultaten wissen
			self.manager.screens[5].teller = 0
			self.manager.screens[5].Score_quizz = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[4].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []

			# ga naar college symbols-scherm
			self.manager.current = "collegenamesscreen"
			self.manager.transition = WipeTransition(duration=1)

		elif self.Trainingskeuze == "Personal Advice":

			# zet gekozen knop "uit"
			self.ids._advice_college.active = False
			# reset tellers
			self.Trainingskeuze = ""
			#self.ids._ButtonStart.text = "Choose"
			self.ids._ButtonStart.text = str(self.knoptext[0][0])

			# bij eerder gespeelde kwis alle resultaten wissen
			self.manager.screens[5].teller = 0
			self.manager.screens[5].Score_quizz = 0
			self.manager.screens[3].Missed_quistions = []
			self.manager.screens[4].Missed_quistions = []
			self.manager.screens[5].Missed_quistions = []
			# ga naar college symbols-scherm
			self.manager.current = "advicescreen"
			self.manager.transition = WipeTransition(duration=1)

		elif self.Trainingskeuze == "":
			self.manager.Popup_Choose("a test module")