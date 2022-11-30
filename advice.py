import sqlite3
from kivy.properties import StringProperty, NumericProperty,ListProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.spinner import Spinner

class MyHooverSpin(Spinner):

	def __int__(self,**kwargs):
		super(MyHooverSpin).__init__(**kwargs)
		Window.bind(mouse_pos=self.on_mouseover)

	def on_mouseover(self,window,pos):
		if self.collide_point(*pos):
			print(*pos)
			print("hoovered!!!!!!!!!!!")

class AdviceScreen(Screen):

	Score_quizz = NumericProperty()
	Missed_questions = ListProperty([])
	teller = NumericProperty()
	tel=NumericProperty()

	def on_enter(self, *args):

		conn = sqlite3.connect("masterresults.db")
		c = conn.cursor()
		c.execute("SELECT Symbolscore FROM masterresults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 1")
		symbooltest = c.fetchone()
		c.execute("SELECT Namescore FROM masterresults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 1")
		namestest = c.fetchone()
		c.execute("SELECT Meaningscore,Time FROM masterresults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 1")
		meaningtest = c.fetchone()
		self.ids.pie_symbols.level= symbooltest[0]
		self.ids.pie_names.level = namestest[0]
		self.ids.pie_meaning.level = meaningtest[0]
		conn.commit()
		conn.close()

	def on_leave(self, *args):

		# leeg alle (mogelijke) rune-mistakes
		self.advice=[]
		self.advice_symbol=[]
		self.advice_names=[]
		self.advice_meaning=[]
		self.advice_names_text= []
		self.advice_meaning_text= []

		# verwijder mistake-runes in tabel
		self.cleaner()
		self.database_size()

	def database_size(self):

		conn = sqlite3.connect("masterresults.db")
		self.c = conn.cursor()

		# aantal afgenomen testen (per categorie) bepalen
		self.c.execute("SELECT COUNT(*),SUM(Symboltraining), SUM(Nametraining), SUM(Meaningtraining) FROM masterresults")
		counts = self.c.fetchall()
		self.c.execute("SELECT COUNT(*) FROM Advice WHERE Testtype = 'Symbol' ")
		self.db_symbol = self.c.fetchone()
		self.c.execute("SELECT COUNT(*) FROM Advice WHERE Testtype = 'Names' ")
		self.db_names = self.c.fetchone()
		self.c.execute("SELECT COUNT(*) FROM Advice WHERE Testtype = 'Meaning' ")
		self.db_meaning = self.c.fetchone()

		self.dataSymbol= self.db_symbol[0]
		self.dataNames= self.db_names[0]
		self.dataMeaning= self.db_meaning[0]

		# beperkt de omvang van de database tot 15 test per categorie
		max= 19

		if self.dataSymbol>max:
			self.c.execute("DELETE FROM Advice WHERE rowid in (SELECT rowid FROM Advice WHERE Testtype = 'Symbol' ORDER BY rowid DESC LIMIT 4)")
		else:
			pass
		if self.dataNames>max:
			self.c.execute("DELETE FROM Advice WHERE rowid in (SELECT rowid FROM Advice WHERE Testtype = 'Names' ORDER BY rowid DESC LIMIT 4)")
		else:
			pass

		if self.dataMeaning>max:
			self.c.execute("DELETE FROM Advice WHERE rowid in (SELECT rowid FROM Advice WHERE Testtype = 'Meaning' ORDER BY rowid DESC LIMIT 4)")
		else:
			pass

		conn.commit()
		conn.close()

	def cleaner(self):
		self.ids._mistake_rune1.text = "-"
		self.ids._mistake_type1.text="info"
		self.ids._mistake_type1.values =""
		self.ids._mistake_perc1.text = "-"
		self.ids._mistake_rune2.text = "-"
		self.ids._mistake_type2.text="info"
		self.ids._mistake_type2.values = ""
		self.ids._mistake_perc2.text = "-"
		self.ids._mistake_rune3.text = "-"
		self.ids._mistake_type3.text="info"
		self.ids._mistake_type3.values = ""
		self.ids._mistake_perc3.text = "-"
		self.ids._mistake_rune4.text = "-"
		self.ids._mistake_type4.text="info"
		self.ids._mistake_type4.values = ""
		self.ids._mistake_perc4.text = "-"
		self.ids._mistake_rune5.text = "-"
		self.ids._mistake_type5.text="info"
		self.ids._mistake_type5.values = ""
		self.ids._mistake_perc5.text = "-"
		self.ids._mistake_rune6.text = "-"
		self.ids._mistake_type6.text="info"
		self.ids._mistake_type6.values = ""
		self.ids._mistake_perc6.text = "-"
		self.ids._mistake_rune7.text = "-"
		self.ids._mistake_type7.text="info"
		self.ids._mistake_type7.values = ""
		self.ids._mistake_perc7.text = "-"

	def display_advice(self, advice,adv2):

		try:
			self.ids._mistake_rune1.text = str(advice[0][0])
			self.ids._mistake_type1.values = adv2[0]
			self.ids._mistake_perc1.text = str(advice[0][1])

			self.ids._mistake_rune2.text = str(advice[1][0])
			self.ids._mistake_type2.values = adv2[1]
			self.ids._mistake_perc2.text = str(advice[1][1])

			self.ids._mistake_rune3.text = str(advice[2][0])
			self.ids._mistake_type3.values = adv2[2]
			self.ids._mistake_perc3.text = str(advice[2][1])

			self.ids._mistake_rune4.text = str(advice[3][0])
			self.ids._mistake_type4.values = adv2[3]
			self.ids._mistake_perc4.text = str(advice[3][1])

			self.ids._mistake_rune5.text = str(advice[4][0])
			self.ids._mistake_type5.values = adv2[4]
			self.ids._mistake_perc5.text = str(advice[4][1])

			self.ids._mistake_rune6.text = str(advice[5][0])
			self.ids._mistake_type6.values = adv2[5]
			self.ids._mistake_perc6.text = str(advice[5][1])

			self.ids._mistake_rune7.text = str(advice[6][0])
			self.ids._mistake_type7.values = adv2[6]
			self.ids._mistake_perc7.text = str(advice[6][1])

		except:
			pass


	def advicer(self, type_advice):

		if type_advice=="Symbols":
			conn = sqlite3.connect("masterresults.db")
			c = conn.cursor()
			c.execute("SELECT Rune, COUNT(*) FROM Advice WHERE Testtype = 'Symbol' GROUP BY Rune ORDER BY COUNT(*) DESC LIMIT 7")
			self.advice_symbol= c.fetchall()
			self.cleaner()
			self.advice_symbol_text=["-","-","-","-","-","-","-"]
			self.display_advice(self.advice_symbol,self.advice_symbol_text)
			conn.commit()
			conn.close()

		elif type_advice == "Names":
			self.advice_names_text=[]
			conn = sqlite3.connect("masterresults.db")
			c = conn.cursor()
			c.execute("SELECT Rune, COUNT(*) FROM Advice WHERE Testtype = 'Names' GROUP BY Rune ORDER BY COUNT(*) DESC LIMIT 7")
			self.advice_names= c.fetchall()
			self.cleaner()
			conn.commit()
			conn.close()

			for combi in self.advice_names:
				conn = sqlite3.connect("dataRunistica.db")
				c = conn.cursor()
				c.execute("SELECT RuneCredo FROM Runistica WHERE RuneNaam=(?)", (combi[0],))
				datarune= c.fetchone()
				self.advice_names_text.append(datarune)
				conn.commit()
				conn.close()

			self.display_advice(self.advice_names,self.advice_names_text)

		elif type_advice == "Meaning":
			self.advice_meaning_text = []
			conn = sqlite3.connect("masterresults.db")
			c = conn.cursor()
			c.execute("SELECT Rune, COUNT(*) FROM Advice WHERE Testtype = 'Meaning' GROUP BY Rune ORDER BY COUNT(*) DESC LIMIT 7")
			self.advice_meaning = c.fetchall()
			self.cleaner()
			conn.commit()
			conn.close()

			for combi in self.advice_meaning:
				conn = sqlite3.connect("dataRunistica.db")
				c = conn.cursor()
				c.execute("SELECT RuneText FROM Runistica WHERE RuneNaam=(?)", (combi[0],))
				datarune= c.fetchone()
				self.advice_meaning_text.append(datarune)
				conn.commit()
				conn.close()

			self.display_advice(self.advice_meaning,self.advice_meaning_text)

