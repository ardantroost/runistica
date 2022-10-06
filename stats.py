import sqlite3
import time
from kivy.properties import Clock
#from kivy.core.window import Window
from kivy.uix.screenmanager import Screen


class StatsScreen(Screen):

	def on_enter(self):

		conn = sqlite3.connect("masterresults.db")
		self.c = conn.cursor()

		# aantal afgenomen testen (per categorie)  bepalen
		self.c.execute("SELECT COUNT(*),SUM(Symboltraining), SUM(Nametraining), SUM(Meaningtraining) FROM masterresults")
		counts = self.c.fetchall()
		#self.ids._tests_symbol.text = str(counts [0][1])
		self.ids._tests_names.text = str(counts[0][2])
		self.ids._tests_meaning.text = str(counts[0][3])

		self.timedisplay()
		self.symbols()
		self.names()
		self.meanings()

		# db sluiten >> conn = sqlite3.connect("MasterResults.db")
		conn.commit()
		conn.close()

	def timedisplay(self):

		self.currenttime = time.strftime("%X")
		self.datum = time.strftime("%d-%m-%Y")
		self.ids._currenttime.text = "time  "+self.currenttime [0:5]
		Clock.schedule_interval(self.timeupdate,60)
		self.ids._datetimes.text = self.datum

	def	symbols(self):

		# Test symbolen
		self.c.execute("SELECT Lastvisit FROM masterresults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 1 ")
		symbooltest1 = self.c.fetchone()
		self.ids._lastvisit_symbol.text = str(symbooltest1[0])

		# selectie laatste score Symbolen
		self.c.execute("SELECT Symbolscore,Time FROM masterresults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 1")
		symbooltest1 = self.c.fetchall()
		self.ids._bar_symbol.level= str(symbooltest1[0][0])
		self.ids._speed_symbol.text = str(symbooltest1[0][1]) + "s"

		# laatste 4 gemiddelden SYMBOLEN
		self.c.execute("SELECT SUM (Symboltraining) FROM masterresults WHERE Symbolscore>0")
		cijferSymbol = self.c.fetchone()
		self.ids._tests_symbol.text=str(cijferSymbol[0])

		self.c.execute("SELECT SUM (Symboltraining), ROUND (AVG(Symbolscore),1), ROUND(AVG(Time),1) FROM (SELECT Symboltraining, Symbolscore,Time FROM masterresults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 4)")
		cijferSymbols=self.c.fetchall()

		self.c.execute("SELECT Symbolscore FROM masterresults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 4")
		Symbolscores = self.c.fetchall()

		if len(Symbolscores)==4:
			x1 = (Symbolscores[0][0] + Symbolscores[1][0] +Symbolscores[2][0])/3
			x2 =(Symbolscores[1][0]+Symbolscores[2][0] + Symbolscores[3][0])/3
			self.growth=(x1-x2)/x2*100
			if self.growth > 0:
				self.ids._symbol_progress.color=1,0,1,1
			else:
				self.ids._symbol_progress.color = 1, 0, 0, 1
			a= str(format(self.growth,".1f"))
			self.ids._symbol_progress.text = a + "%"
			self.ids._test1_symbol.level = str((Symbolscores[0][0]) * 10.0)
			self.ids._test2_symbol.level = str((Symbolscores[1][0]) * 10.0)
			self.ids._test3_symbol.level = str((Symbolscores[2][0]) * 10.0)
			self.ids._test4_symbol.level = str((Symbolscores[3][0]) * 10.0)
			self.ids._pie1_symbol.level = ((Symbolscores[0][0] + Symbolscores[1][0] + Symbolscores[2][0] + Symbolscores[3][0])/4) * 36
		elif len(Symbolscores)==3:
			x1 =(Symbolscores[0][0]+Symbolscores[1][0])/2
			x2 =(Symbolscores[1][0] + Symbolscores[2][0])/2
			self.growth=(x1-x2)/x2*100
			a=format(self.growth,".1f")
			if self.growth > 0:
				self.ids._symbol_progress.color=1,0,1,1
			else:
				self.ids._symbol_progress.color = 1, 0, 0, 1
			self.ids._symbol_progress.text = str(a) + "%"
			self.ids._test1_symbol.level = str((Symbolscores[0][0]) * 10.0)
			self.ids._test2_symbol.level = str((Symbolscores[1][0]) * 10.0)
			self.ids._test3_symbol.level = str((Symbolscores[2][0]) * 10.0)
			self.ids._test4_symbol.level = 0
			self.ids._pie1_symbol.level = ((Symbolscores[0][0] + Symbolscores[1][0]+Symbolscores[2][0])/3) * 36

		elif len(Symbolscores)==2:
			x1 =Symbolscores[0][0]
			x2 =Symbolscores[1][0]
			self.growth=(x1-x2)/x2*100
			a= self.growth
			if self.growth > 0:
				self.ids._symbol_progress.color=1,0,1,1
			else:
				self.ids._symbol_progress.color = 1, 0, 0, 1
			ab= str(format(a,".1f"))
			self.ids._symbol_progress.text=str(ab)+"%"

			self.ids._test1_symbol.level = str((Symbolscores[0][0]) * 10.0)
			self.ids._test2_symbol.level = str((Symbolscores[1][0]) * 10.0)
			self.ids._test3_symbol.level = 0
			self.ids._test4_symbol.level = 0
			self.ids._pie1_symbol.level =((Symbolscores[0][0] + Symbolscores[1][0])/2) * 36
		elif len(Symbolscores) == 1:
			self.ids._symbol_progress.text= "No data"
			self.ids._symbol_progress.font_size=9
			self.ids._test1_symbol.level = str((Symbolscores[0][0]) * 10)
			self.ids._test2_symbol.level = 0
			self.ids._test3_symbol.level = 0
			self.ids._test4_symbol.level = 0
			# performance 4 laatste symboltest afbeelden
			self.ids._pie1_symbol.level = (Symbolscores[0][0])*3.6

				#######################################################
	def names(self):

		# Test Namen
		self.c.execute("SELECT Lastvisit FROM masterresults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 1 ")
		nametest2 = self.c.fetchone()
		self.ids._lastvisit_names.text = str(nametest2[0])

		# selectie laatste score Namem
		self.c.execute("SELECT Namescore,Time FROM masterresults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 1")
		symbooltest2 = self.c.fetchall()
		self.ids._bar_names.level = str(symbooltest2[0][0])
		self.ids._speed_names.text = str(symbooltest2[0][1]) + "s"

		# laatste 4 gemiddelden namen
		self.c.execute("SELECT SUM (Nametraining) FROM masterresults WHERE Namescore>0")
		cijfer_Name=self.c.fetchone()


		self.c.execute("SELECT Namescore FROM masterresults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 4")
		Namesscores = self.c.fetchall()

		if len(Namesscores)==4:
			x1 = (Namesscores[0][0] + Namesscores[1][0]+Namesscores[2][0])/3
			x2 = (Namesscores[1][0]+Namesscores[2][0] + Namesscores[3][0])/3
			self.growth=(x1-x2)/x2*100
			if self.growth > 0:
				self.ids._names_progrself.ids._pie1_names.leveless.color=1,0,1,1
			else:
				self.ids._names_progress.color = 1, 0, 0, 1
			a= str(format(self.growth,".1f"))
			self.ids._names_progress.text = a + "%"

			self.ids._test1_names.level = str((Namesscores[0][0]) * 10.0)
			self.ids._test2_names.level = str((Namesscores[1][0]) * 10.0)
			self.ids._test3_names.level = str((Namesscores[2][0]) * 10.0)
			self.ids._test4_names.level = str((Namesscores[3][0]) * 10.0)
			self.ids._pie1_names.level = ((Namesscores[0][0] + Namesscores[1][0] + Namesscores[2][0] + Namesscores[3][0])/4) * 36

		elif len(Namesscores)==3:
			x1 =(Namesscores[0][0]+Namesscores[1][0])/2
			x2 =(Namesscores[1][0] + Namesscores[2][0])/2
			self.growth=(x1-x2)/x2*100
			a=format(self.growth,".1f")
			if self.growth > 0:
				self.ids._names_progress.color=1,0,1,1
			else:
				self.ids._names_progress.color = 1, 0, 0, 1
			self.ids._names_progress.text = str(a) + "%"
			self.ids._test1_names.level = str((Namesscores[0][0]) * 10.0)
			self.ids._test2_names.level = str((Namesscores[1][0]) * 10.0)
			self.ids._test3_names.level = str((Namesscores[2][0]) * 10.0)
			self.ids._test4_names.level = 0
			self.ids._pie1_names.level = ((Namesscores[0][0] + Namesscores[1][0] + Namesscores[2][0])/3) * 36
		elif len(Namesscores)==2:
			x1 =Namesscores[0][0]
			x2 =Namesscores[1][0]
			self.growth=(x1-x2)/x2*100
			a= self.growth
			if self.growth > 0:
				self.ids._names_progress.color=1,0,1,1
			else:
				self.ids._names_progress.color = 1, 0, 0, 1
			ab= str(format(a,".1f"))
			self.ids._names_progress.text=str(ab)+"%"
			self.ids._test1_names.level = str((Namesscores[0][0]) * 10.0)
			self.ids._test2_names.level = str((Namesscores[1][0]) * 10.0)
			self.ids._test3_names.level = 0
			self.ids._test4_names.level = 0
			self.ids._pie1_names.level = ((Namesscores[0][0] + Namesscores[1][0])/ 2) * 36
		elif len(Namesscores) == 1:
			self.ids._names_progress.text= "No data"
			self.ids._names_progress.font_size=9
			self.ids._test1_names.level = str((Namesscores[0][0]) * 10.0)
			self.ids._test2_names.level = 0
			self.ids._test3_names.level = 0
			self.ids._test4_names.level = 0
			self.ids._pie1_names.level = 0
		#######################################################

	def meanings(self):

		self.c.execute("SELECT Lastvisit FROM masterresults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 1 ")
		symbooltest3 = self.c.fetchone()
		self.ids._lastvisit_meaning.text = str(symbooltest3[0])

		# score meaning
		self.c.execute("SELECT Meaningscore,Time FROM masterresults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 1")
		symbooltest3 = self.c.fetchall()
		#self.ids._meaning2_score.text = str(symbooltest3[0][0])
		self.ids._bar_meaning.level = str(symbooltest3[0][0])
		self.ids._speed_meaning.text = str(symbooltest3[0][1]) + "s"

		#laatste 4 gemiddelden meaning
		self.c.execute("SELECT SUM (Meaningtraining) FROM masterresults WHERE Meaningscore>0")
		cijfer_Meaning=self.c.fetchone()

		#self.c.execute("SELECT ROUND (AVG(Meaningscore),1), ROUND(AVG(Time),1) FROM (SELECT Meaningscore,Time FROM MasterResults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 4)")
		#cijfer_Meaning1 = self.c.fetchall()
		#print("aantal testen Meaning: "+ str(cijfer_Meaning[0]) + "testgemiddelde Meaningtraining: " + str(cijfer_Meaning1[0][0]))
		#self.ids._meaning1.text= str(cijfer_Meaning[0])
		#self.ids._meaning3_score.text = str(cijfer_Meaning1[0][0])
		#self.ids._meaning4_speed.text = str(cijfer_Meaning1[0][1])

		self.c.execute("SELECT Meaningscore FROM masterresults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 4")
		Meaningscores = self.c.fetchall()

		if len(Meaningscores)==4:
			x1 = (Meaningscores[0][0] + Meaningscores[1][0]+Meaningscores[2][0])/3
			x2 =(Meaningscores[1][0]+Meaningscores[2][0] + Meaningscores[3][0])/3
			self.growth=(x1-x2)/x2*100
			a= str(format(self.growth,".1f"))
			if self.growth > 0:
				self.ids._meaning_progress.color=1,0,1,1
			else:
				self.ids._meaning_progress.color = 1, 0, 0, 1

			self.ids._meaning_progress.text = a + "%"
			self.ids._test1_meaning.level = str((Meaningscores[0][0]) * 10)
			self.ids._test2_meaning.level = str((Meaningscores[1][0]) * 10)
			self.ids._test3_meaning.level = str((Meaningscores[2][0]) * 10)
			self.ids._test4_meaning.level = str((Meaningscores[3][0]) * 10)
			self.ids._pie1_meaning.level = ((Meaningscores[0][0] + Meaningscores[1][0] + Meaningscores[2][0] + Meaningscores[3][0])/ 4) * 36
		elif len(Meaningscores)==3:
			x1 =(Meaningscores[0][0]+Meaningscores[1][0])/2
			x2 =(Meaningscores[1][0] + Meaningscores[2][0])/2
			self.growth=(x1-x2)/x2*100
			a=format(self.growth,".1f")
			if self.growth > 0:
				self.ids._meaning_progress.color=1,0,1,1
			else:
				self.ids._meaning_progress.color = 1, 0, 0, 1
			self.ids._meaning_progress.text = str(a) + "%"
			self.ids._test1_meaning.level = str((Meaningscores[0][0]) * 10)
			self.ids._test2_meaning.level = str((Meaningscores[1][0]) * 10)
			self.ids._test3_meaning.level = str((Meaningscores[2][0]) * 10)
			self.ids._test4_meaning.level = 0
			self.ids._pie1_meaning.level = ((Meaningscores[0][0] + Meaningscores[1][0] + Meaningscores[2][0])/ 3) * 36
		elif len(Meaningscores)==2:
			x1 =Meaningscores[0][0]
			x2 =Meaningscores[1][0]
			self.growth=(x1-x2)/x2*100
			a= self.growth
			ab= str(format(a,".1f"))
			self.ids._meaning_progress.text=str(ab)+"%"

			if self.growth > 0:
				self.ids._meaning_progress.color=1,0,1,1
			else:
				self.ids._meaning_progress.color = 1, 0, 0, 1

			self.ids._test1_meaning.level = str((Meaningscores[0][0]) * 10)
			self.ids._test2_meaning.level = str((Meaningscores[1][0]) * 10)
			self.ids._test3_meaning.level = 0
			self.ids._test4_meaning.level = 0
			self.ids._pie1_meaning.level = ((Meaningscores[0][0] + Meaningscores[1][0])/ 2) * 36

		elif len(Meaningscores) == 1:
			self.ids._meaning_progress.text= "No data"
			self.ids._meaning_progress.font_size=9
			self.ids._test1_meaning.level = str((Meaningscores[0][0]) * 10)
			self.ids._test2_meaning.level = 0
			self.ids._test3_meaning.level = 0
			self.ids._test4_meaning.level = 0
			self.ids._pie1_meaning.level =0

			#self.ids._bar_meaning.level =  (cijfer_Meaning1[0][0])/10*100
		#self.ids._bar_meaning.text = format(((cijfer_Meaning1[0][0]) / 10 * 100),".1f") + "%"


	def timeupdate(self, *args):

		self.currenttime = time.strftime("%X")
		self.ids._currenttime.text = self.currenttime[0:5]


	def on_leave(self):
		pass

