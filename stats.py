import sqlite3
import time
from kivy.properties import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class StatsScreen(Screen):

	def on_enter(self):

		conn = sqlite3.connect("masterresults.db")
		self.c = conn.cursor()

		# aantal afgenomen testen (per categorie) bepalen
		self.c.execute("SELECT COUNT(*),SUM(Symboltraining), SUM(Nametraining), SUM(Meaningtraining) FROM masterresults")
		counts = self.c.fetchall()
		self.ids._tests_symbol.text = str(counts [0][1])
		self.ids._tests_names.text = str(counts[0][2])
		self.ids._tests_meaning.text = str(counts[0][3])

		# beperkt de omvang van de database tot 6 test per categorie

		self.maximaal= 10

		if counts[0][1] >= self.maximaal:
			self.del_database("symbol")
		elif counts[0][2] >=self.maximaal:
			self.del_database("names")
		elif counts[0][3] >=self.maximaal:
			self.del_database("meaning")

		self.timedisplay()
		self.symbols()
		self.names()
		self.meanings()

		# db sluiten >> conn = sqlite3.connect("MasterResults.db") na on_enter-display
		conn.commit()
		conn.close()

	def del_database(self,testtype):

		# verwijder laatste 4 tests als er meer dan 10( =self.maximaal) tests zijn in een categorie

		conn = sqlite3.connect("masterresults.db")
		c = conn.cursor()
		if testtype == "symbol":
			c.execute("DELETE FROM masterresults WHERE rowid in (SELECT rowid FROM masterresults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 4)")

		elif testtype =="names":
			c.execute("DELETE FROM masterresults WHERE rowid in (SELECT rowid FROM masterresults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 4)")

		elif testtype == "meaning":
			c.execute("DELETE FROM masterresults WHERE rowid in (SELECT rowid FROM masterresults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 4)")

		self.c.execute("SELECT COUNT(*),SUM(Symboltraining), SUM(Nametraining), SUM(Meaningtraining) FROM masterresults")
		counts = self.c.fetchall()

		self.ids._tests_symbol.text = str(counts [0][1])
		self.ids._tests_names.text = str(counts[0][2])
		self.ids._tests_meaning.text = str(counts[0][3])

		# na verwijdering actie...
		# opslaan en sluiten van database
		conn.commit()
		conn.close()

	def infodisplay(self):
		self.manager.Popup_infomaster()

	def score_deleter(self,instance, instructie):

		conn = sqlite3.connect("masterresults.db")
		c = conn.cursor()

		if instructie == "lastsymbol":
			c.execute("DELETE FROM masterresults WHERE rowid in (SELECT rowid FROM masterresults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 1)")
		elif instructie == "lastnames":
			c.execute("DELETE FROM masterresults WHERE rowid in (SELECT rowid FROM masterresults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 1)")

		elif instructie == "lastmeaning":
			c.execute("DELETE FROM masterresults WHERE rowid in (SELECT rowid FROM masterresults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 1)")

		elif instructie == "allsymbols":
			c.execute("DELETE FROM masterresults WHERE Symboltraining=1")

		elif instructie == "allnames":
			c.execute("DELETE FROM masterresults WHERE Nametraining=1")

		elif instructie == "allmeaning":
			c.execute("DELETE FROM masterresults WHERE Meaningtraining=1")

		elif instructie == "all":

			# popup met keuzeopties voor deletes verwijderen
			self.manager.Popuppie_buttons.dismiss()
			# popup-waarschuwing alles verwijderen
			self.manager.Popup_delete_warning()

		# na actie...
		# sluiten van database
		conn.commit()
		conn.close()

		# opschonen van de pagina
		self.on_enter()

	def on_press_button(self,event):

		# bij selectie wordt tekstbutton "paars"
		event.color=(1,0,1,1)

	def displaydelete(self):

		self.b1 = BoxLayout(orientation="vertical", spacing=20, padding=20)

		self.Label_last_test = Label(text="Last score of one test", color=[1,0,1,1], font_size=22, halign="center", size_hint=(1,.1))
		self.Label_all_test  = Label(text="All scores of a whole test category",color=[1,0,1,1],font_size=22, halign="center", size_hint=(1,.1))
		self.Label_all       = Label(text="All test scores", color=[1,0,1,1],font_size=22, halign="center", size_hint=(1,.1))

		self.g1 = GridLayout(cols=3)
		self.g2 = GridLayout(cols=3)
		self.g3 = GridLayout(cols=3)

		self.b_delete_last_symbols = BoxLayout(orientation="vertical", spacing=5)
		self.image_delete_last_symbols = Image(source="Pics/delete.png", pos=self.pos)
		self.button_delete_last_symbols = Button(text="Symbol test\nonly last score",on_press= self.on_press_button,font_size=20, halign="center",color=[0,0,0,.75],background_color=[0,0,0,0])
		self.button_delete_last_symbols.bind(on_release= lambda instance:self.score_deleter(instance,"lastsymbol"))

		self.b_delete_last_symbols.add_widget(self.image_delete_last_symbols)
		self.b_delete_last_symbols.add_widget(self.button_delete_last_symbols)
		self.g1.add_widget(self.b_delete_last_symbols)

		self.b_delete_last_names = BoxLayout(orientation="vertical",spacing=5)
		self.image_delete_last_names = Image(source="Pics/delete.png", pos=self.pos)
		self.button_delete_last_names = Button(text="Names test\nonly last score",on_press= self.on_press_button, font_size=20,halign="center",color=[0,0,0,.75],background_color=[0,0,0,0])
		self.button_delete_last_names.bind(on_release=lambda instance:self.score_deleter(instance,"lastnames"))
		self.b_delete_last_names.add_widget(self.image_delete_last_names)
		self.b_delete_last_names.add_widget(self.button_delete_last_names)
		self.g1.add_widget(self.b_delete_last_names)

		self.b_delete_last_meaning = BoxLayout(orientation="vertical",spacing=5)
		self.image_delete_last_meaning= Image(source="Pics/delete.png", pos=self.pos)
		self.button_delete_last_meaning = Button(text="Meaning test\n only last score", on_press= self.on_press_button,font_size=20,halign="center",color=[0,0,0,.75],background_color=[0,0,0,0])
		self.button_delete_last_meaning.bind(on_release=lambda instance:self.score_deleter(instance,"lastmeaning"))
		self.b_delete_last_meaning.add_widget(self.image_delete_last_meaning)
		self.b_delete_last_meaning.add_widget(self.button_delete_last_meaning)
		self.g1.add_widget(self.b_delete_last_meaning)

		self.b_delete_all_symbols = BoxLayout(orientation="vertical",spacing=5)
		self.image_delete_all_symbols = Image(source="Pics/delete.png", pos=self.pos)
		self.button_delete_all_symbols = Button(text="Symbol tests\nall scores",on_press= self.on_press_button ,font_size=20,halign="center",color=[0,0,0,1],background_color=[0,0,0,0])
		self.button_delete_all_symbols.bind(on_release=lambda instance: self.score_deleter(instance, "allsymbols"))
		self.b_delete_all_symbols.add_widget(self.image_delete_all_symbols)
		self.b_delete_all_symbols.add_widget(self.button_delete_all_symbols)
		self.g2.add_widget(self.b_delete_all_symbols)

		self.b_delete_all_names = BoxLayout(orientation="vertical",spacing=5)
		self.image_delete_all_names = Image(source="Pics/delete.png", pos=self.pos)
		self.button_delete_all_names = Button(text="Names tests\nall scores",on_press= self.on_press_button, font_size=20,halign="center",color=[0,0,0,1],background_color=[0,0,0,0])
		self.button_delete_all_names.bind(on_release=lambda instance: self.score_deleter(instance, "allnames"))
		self.b_delete_all_names.add_widget(self.image_delete_all_names)
		self.b_delete_all_names.add_widget(self.button_delete_all_names)
		self.g2.add_widget(self.b_delete_all_names)

		self.b_delete_all_meaning = BoxLayout(orientation="vertical",spacing=5)
		self.image_delete_all_meaning = Image(source="Pics/delete.png", pos=self.pos)
		self.button_delete_all_meaning = Button(text="Meaning tests\nall scores",on_press= self.on_press_button, font_size=20,halign="center",color=[0,0,0,1],background_color=[0,0,0,0])
		self.button_delete_all_meaning.bind(on_release=lambda instance: self.score_deleter(instance, "allmeaning"))
		self.b_delete_all_meaning.add_widget(self.image_delete_all_meaning)
		self.b_delete_all_meaning.add_widget(self.button_delete_all_meaning)
		self.g2.add_widget(self.b_delete_all_meaning)

		self.b_delete_all = BoxLayout(orientation="vertical",spacing=5)
		self.image_delete_all=Image(source="Pics/delete.png",pos=self.pos)
		self.button_delete_all=Button(text="All\ntest scores",on_press= self.on_press_button, font_size=20,halign="center",color=[0,0,0,1],background_color=[0,0,0,0])
		self.button_delete_all.bind(on_release=lambda instance: self.score_deleter(instance, "all"))
		self.b_delete_all.add_widget(self.image_delete_all)
		self.b_delete_all.add_widget(self.button_delete_all)
		self.g3.add_widget(self.b_delete_all)

		self.b1.add_widget(self.Label_last_test)
		self.b1.add_widget(self.g1)
		self.b1.add_widget(self.Label_all_test)
		self.b1.add_widget(self.g2)
		self.b1.add_widget(self.Label_all)
		self.b1.add_widget(self.g3)

		self.manager.Popup_delete_options(self.b1)

	def timedisplay(self):

		self.currenttime = time.strftime("%X")
		self.datum = time.strftime("%d-%m-%Y")
		self.ids._currenttime.text = "time  "+ self.currenttime[0:5]
		Clock.schedule_interval(self.timeupdate,1)
		self.ids._datetimes.text = self.datum

	def	symbols(self):

		self.c.execute("SELECT Lastvisit FROM masterresults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 1 ")
		symbooltest1 = self.c.fetchall()

		if len(symbooltest1)>0:
			self.ids._lastvisit_symbol.text = str(symbooltest1[0][0])
		else:
			self.ids._lastvisit_symbol.text = ""

		# selectie laatste score Symbol-test
		self.c.execute("SELECT Symbolscore,Time FROM masterresults WHERE Symbolscore>0 ORDER BY rowid DESC LIMIT 1")
		symbooltest1 = self.c.fetchall()
		if len(symbooltest1) > 0:
			self.ids._bar_symbol.level= str(symbooltest1[0][0])
			self.ids._speed_symbol.text = str(symbooltest1[0][1]) + "s"

		else:
			self.ids._bar_symbol.level = 0

		# laatste 4 gemiddelden SYMBOLEN
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
			self.ids._pie1_symbol.level = ((Symbolscores[0][0] + Symbolscores[1][0] + Symbolscores[2][0] + Symbolscores[3][0])/4)*36
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
			self.ids._pie1_symbol.level = (Symbolscores[0][0])*36

		elif len(Symbolscores) == 0:
			self.ids._symbol_progress.text= "No data"
			self.ids._symbol_progress.font_size=9
			self.ids._test1_symbol.level = 0
			self.ids._test2_symbol.level = 0
			self.ids._test3_symbol.level = 0
			self.ids._test4_symbol.level = 0
			# performance 4 laatste symboltest afbeelden
			self.ids._pie1_symbol.level = 0
	########################################################################################################

	def names(self):
		# Test Namen
		self.c.execute("SELECT Lastvisit FROM masterresults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 1 ")
		nametest2 = self.c.fetchall()
		if len(nametest2)>0:
			self.ids._lastvisit_names.text = str(nametest2[0][0])
		else:
			self.ids._lastvisit_names.text = ""

		# selectie laatste score Names
		self.c.execute("SELECT Namescore,Time FROM masterresults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 1")
		symbooltest2 = self.c.fetchall()
		if len(symbooltest2) > 0:
			self.ids._bar_names.level = str(symbooltest2[0][0])
			self.ids._speed_names.text = str(symbooltest2[0][1]) + "s"
		else:
			self.ids._bar_names.level = 0

		# aantal testen names training
		self.c.execute("SELECT SUM (Nametraining) FROM masterresults WHERE Namescore>0")
		cijfer_Name=self.c.fetchone()
		# laatste 4 gemiddelden namen
		self.c.execute("SELECT Namescore FROM masterresults WHERE Namescore>0 ORDER BY rowid DESC LIMIT 4")

		Namesscores = self.c.fetchall()

		if len(Namesscores)==4:
			x1 = (Namesscores[0][0] + Namesscores[1][0]+Namesscores[2][0])/3
			x2 = (Namesscores[1][0]+Namesscores[2][0] + Namesscores[3][0])/3
			self.growth=(x1-x2)/x2*100
			if self.growth > 0:
				self.ids._names_progress.color =1,0,1,1
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
			self.ids._pie1_names.level  = 0
			self.ids._pie1_names.level = (Namesscores[0][0] * 36)
		elif len(Namesscores) == 0:
			self.ids._names_progress.text = "No data"
			self.ids._names_progress.font_size = 9
			self.ids._test1_names.level = 0
			self.ids._test2_names.level = 0
			self.ids._test3_names.level = 0
			self.ids._test4_names.level = 0
			self.ids._pie1_names.level  = 0
		#######################################################
	def meanings(self):
		#test meaning of runes

		self.c.execute("SELECT Lastvisit FROM masterresults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 1 ")
		self.symbooltest3 = self.c.fetchall()

		if len(self.symbooltest3)>0:
			self.ids._lastvisit_meaning.text = str(self.symbooltest3[0][0])
		else:
			self.ids._lastvisit_meaning.text = ""

		# score meaning
		self.c.execute("SELECT Meaningscore,Time FROM masterresults WHERE Meaningscore>0 ORDER BY rowid DESC LIMIT 1")
		self.symbooltest3 = self.c.fetchall()

		if len(self.symbooltest3)>0:
			self.ids._bar_meaning.level = str(self.symbooltest3[0][0])
			self.ids._speed_meaning.text = str(self.symbooltest3[0][1]) + "s"
		else:
			self.ids._bar_meaning.level = 0

		#laatste 4 gemiddelden meaning
		self.c.execute("SELECT SUM (Meaningtraining) FROM masterresults WHERE Meaningscore>0")
		cijfer_Meaning=self.c.fetchone()

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
			self.ids._pie1_meaning.level = Meaningscores[0][0] * 36

		elif len(Meaningscores) == 0:
			self.ids._meaning_progress.text= "No data"
			self.ids._meaning_progress.font_size=9
			self.ids._test1_meaning.level = 0
			self.ids._test2_meaning.level = 0
			self.ids._test3_meaning.level = 0
			self.ids._test4_meaning.level = 0
			self.ids._pie1_meaning.level =0

	def timeupdate(self, *args):

		self.currenttime = time.strftime("%X")
		self.ids._currenttime.text = "Time "+ self.currenttime[0:5]

	def on_leave(self):
		pass


