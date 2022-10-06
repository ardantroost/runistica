import sqlite3
import time

from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty,Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import random


class StatsScreen(Screen):

	def on_enter(self):

		conn = sqlite3.connect("MasterResults.db")
		self.c = conn.cursor()

		# aantal afgenomen testen (per categorie)  bepalen
		self.c.execute("SELECT COUNT(*),SUM(Symboltraining), SUM(Nametraining), SUM(Meaningtraining) FROM MasterResults")
		counts = self.c.fetchall()
		print("aantal gehouden testen & aantal per test: " + str(counts))

		self.timedisplay()
		self.symbols()
		self.names()
		self.meanings()

		# db sluiten
		#conn = sqlite3.connect("MasterResults.db")
		conn.commit()
		conn.close()

	def timedisplay(self):

		self.currenttime = time.strftime("%X")
		self.ids._currenttime.text = self.currenttime[0:5]
		Clock.schedule_interval(self.timeupdate,60)

		self.datum = time.strftime("%d-%m-%Y")
		self.ids._datetimes.text = self.datum

	def assesment_master(self, valueSymbol,valueNames, valueMeaning):

		if valueSymbol!=0:
			if valueSymbol >9:
				self.ids._symbol4_level.text = "Master of runes"
				self.ids._bar_symbol.color = 0, 1, 0, 1

			elif valueSymbol <5:
				self.ids._symbol4_level.text = "Apprentice"
				self.ids._bar_symbol.color=1,0,0,1
			else:
				self.ids._symbol4_level.text = "Medior Master"
				self.ids._bar_symbol.color = 255/255,69/255,0,1

		elif valueNames != 0:

			if valueNames >=9:
				self.ids._names4_level.text = "Master of runes"
			elif valueNames <=5:
				self.ids._names4_level.text = "Apprentice"
			else:
				self.ids._names4_level.text = "Medior Master"

		elif valueMeaning!=0:

			if valueMeaning >=9:
				self.ids._meaning4_level.text = "Master of runes"
			elif valueMeaning <=5:
				self.ids._meaning4_level.text = "Apprentice"
			else:
				self.ids._meaning4_level.text = "Medior Master"

	def	symbols(self):

		# Test symbolen
		self.c.execute("SELECT Lastvisit FROM MasterResults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 1 ")
		symbooltest1 = self.c.fetchone()
		self.ids._symbol.text = str(symbooltest1[0])

		# selectie laatste score Symbolen
		self.c.execute("SELECT Symbolscore,Time FROM MasterResults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 1")
		symbooltest1 = self.c.fetchall()
		self.ids._symbol2_score.text= str(symbooltest1[0][0])
		self.ids._symbol_speed.text = str(symbooltest1[0][1])

		# laatste 4 gemiddelden SYMBOLEN
		self.c.execute("SELECT SUM (Symboltraining) FROM MasterResults WHERE Symbolscore>0")
		cijferSymbol = self.c.fetchone()
		self.c.execute("SELECT SUM (Symboltraining), ROUND (AVG(Symbolscore),1), ROUND(AVG(Time),1) FROM (SELECT Symboltraining, Symbolscore,Time FROM MasterResults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 4)")
		cijferSymbols=self.c.fetchall()
		print("aantal symbooltesten :"+ str(cijferSymbol[0])+ ", testgemiddelde Symbooltraining: "+str(cijferSymbols[0][1]))
		self.ids._symbol1.text= str(cijferSymbol[0])
		self.ids._symbol3_score.text = str(cijferSymbols[0][1])
		self.ids._symbol4_speed.text = str(cijferSymbols[0][2])

		self.ids._bar_symbol.level =  (cijferSymbols[0][1])/10*100
		self.ids._bar_symbol.text = format(((cijferSymbols[0][1]) / 10 * 100),".1f") + "%"

		# bepaal en print masterdegree
		self.assesment_master(valueSymbol=cijferSymbols[0][1], valueNames=0, valueMeaning=0)

		##################################################

	def names(self):

		# Test Namen
		self.c.execute("SELECT Lastvisit FROM MasterResults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 1 ")
		symbooltest2 = self.c.fetchone()
		self.ids._name.text = str(symbooltest2[0])
		# selectie laatste score Namem
		self.c.execute("SELECT Namescore,Time FROM MasterResults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 1")
		symbooltest2 = self.c.fetchall()
		self.ids._name2_score.text = str(symbooltest2[0][0])
		self.ids._name_speed.text = str(symbooltest2[0][1])

		# laatste 4 gemiddelden namen
		self.c.execute("SELECT SUM (Nametraining) FROM MasterResults WHERE Namescore>0")
		cijfer_Name=self.c.fetchone()
		self.c.execute("SELECT ROUND (AVG(Namescore),1), ROUND(AVG(Time),1) FROM (SELECT Namescore,Time FROM MasterResults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 4)")
		cijfer_Names=self.c.fetchall()
		print("aantal testen Namen: "+ str(cijfer_Name[0])+ "testgemiddelde Namen: "+str(cijfer_Names[0]))
		self.ids._name1.text = str(cijfer_Name[0])
		self.ids._name3_score.text = str(cijfer_Names[0][0])
		self.ids._name4_speed.text = str(cijfer_Names[0][1])

		self.ids._bar_name.level = (cijfer_Names[0][0]) / 10 * 100
		self.ids._bar_name.text = format(((cijfer_Names[0][0]) / 10 * 100), ".1f") + "%"

		# bepaal en print masterdegree
		self.assesment_master(valueSymbol=0, valueNames=cijfer_Names[0][0], valueMeaning=0)

		#######################################################

	def meanings(self):

		self.c.execute("SELECT Lastvisit FROM MasterResults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 1 ")
		symbooltest3 = self.c.fetchone()
		self.ids._meaning.text = str(symbooltest3[0])

		# score mmeaning
		self.c.execute("SELECT Meaningscore,Time FROM MasterResults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 1")
		symbooltest3 = self.c.fetchall()
		self.ids._meaning2_score.text = str(symbooltest3[0][0])
		self.ids._meaning_speed.text = str(symbooltest3[0][1])

		#laatste 4 gemiddelden meaning
		self.c.execute("SELECT SUM (Meaningtraining) FROM MasterResults WHERE Meaningscore>0")
		cijfer_Meaning=self.c.fetchone()
		self.c.execute("SELECT ROUND (AVG(Meaningscore),1), ROUND(AVG(Time),1) FROM (SELECT Meaningscore,Time FROM MasterResults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 4)")
		cijfer_Meaning1 = self.c.fetchall()
		print("aantal testen Meaning: "+ str(cijfer_Meaning[0]) + "testgemiddelde Meaningtraining: " + str(cijfer_Meaning1[0][0]))
		self.ids._meaning1.text= str(cijfer_Meaning[0])
		self.ids._meaning3_score.text = str(cijfer_Meaning1[0][0])
		self.ids._meaning4_speed.text = str(cijfer_Meaning1[0][1])

		self.ids._bar_meaning.level =  (cijfer_Meaning1[0][0])/10*100
		self.ids._bar_meaning.text = format(((cijfer_Meaning1[0][0]) / 10 * 100),".1f") + "%"

		self.assesment_master(valueSymbol=0, valueNames=0, valueMeaning=cijfer_Meaning1[0][0])

	def timeupdate(self, *args):

		self.currenttime = time.strftime("%X")
		self.ids._currenttime.text = self.currenttime[0:5]


	def on_leave(self):
		pass

