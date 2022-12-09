import sqlite3
from kivy.properties import StringProperty, NumericProperty,ListProperty
from kivy.uix.screenmanager import Screen,RiseInTransition


class ResultScreen(Screen):

	Score_quizz = NumericProperty()
	Missed_quistions = ListProperty([])
	Missed_runes = ListProperty([])
	teller = NumericProperty()
	tel=NumericProperty()
	indicator = StringProperty("")
	lanquage= StringProperty("")

	def on_leave(self, *args):

		self.teller= 0
		self.Missed_quistions=[]
		self.Missed_runes=[]
		self.Score_quizz = 0
		self.tel=0
		self.indicator= ""
		self.resulttexten = ""

	def on_enter(self, *args):

		resulttexten=[]

		self.lanquage = self.manager.lanquage
		conn = sqlite3.connect("taalkeuze.db")
		c = conn.cursor()

		if self.lanquage == 'Engels':
			c.execute("SELECT Header, text1, text2, text3, button, end FROM result WHERE taal=(?)",("Engels",))
			resulttexten = c.fetchall()
		elif self.lanquage == 'Frans':
			c.execute("SELECT Header, text1, text2, text3, button, end FROM result WHERE taal=(?)",("Frans",))
			resulttexten = c.fetchall()
		elif self.lanquage == 'Duits':
			c.execute("SELECT Header, text1, text2, text3, button, end FROM result WHERE taal=(?)",("Duits",))
			resulttexten = c.fetchall()
		elif self.lanquage == 'Nederlands':
			c.execute("SELECT Header, text1, text2, text3, button, end FROM result WHERE taal=(?)",("Nederlands",))
			resulttexten = c.fetchall()

		conn.commit()
		conn.close()

		self.resulttexten = resulttexten

	def Display_Results(self,next):

		if len(self.manager.get_screen("vragenscreen").Missed_quistions) > 0:
			self.Missed_quistions = self.manager.get_screen("vragenscreen").Missed_quistions
			self.indicator = "RuneNaam"
		elif len(self.manager.get_screen("vragenscreeneen").Missed_quistions)>0:
			self.Missed_quistions = self.manager.get_screen("vragenscreeneen").Missed_quistions
			self.indicator = "RuneCredo"
		elif len(self.manager.get_screen("vragenscreentwee").Missed_quistions)>0:
			self.Missed_quistions = self.manager.get_screen("vragenscreentwee").Missed_quistions
			self.indicator = "RuneText"
		# als er geen missed.quistions zijn in alle trainingskeuzes (dus "0" zijn => foutloze testscore)
		else:
			self.manager.current = "menuscreen"
			self.manager.transition = RiseInTransition(duration=1)

		self.DisplaySelection = []

		for i in self.Missed_quistions:

			conn = sqlite3.connect("dataRunistica.db")
			c = conn.cursor()
			c.execute("SELECT RuneNaam,RuneCredo, RuneText, Signtype FROM Runistica WHERE "+f'{self.indicator}'+"=(?)", (i,))
			xyz= c.fetchall()
			self.DisplaySelection.append(xyz)
			conn.commit()
			conn.close()

		einde = len(self.Missed_quistions)

		if self.tel < einde:
			self.ids._ResultNaam.text =""
			self.ids._MissedRune.text = str(self.DisplaySelection[self.tel][0][0])
			self.ids._MissedRuneNaam.source = "Tekens/"+ (str(self.DisplaySelection[self.tel][0][0])).lower()+".png"
			self.ids._AssociationMissedRune.text = str(self.resulttexten[0][1]) + self.DisplaySelection[self.tel][0][1]
			self.ids._AdviceMissedRune.text = str(self.resulttexten[0][2]) + self.DisplaySelection[self.tel][0][2]
			self.ids._FavourMissedRune.text = str(self.resulttexten[0][3]) + self.DisplaySelection[self.tel][0][3]
			self.ids._ButtonAdvice.text = str(self.resulttexten[0][4])

			self.tel += next

		else:
			# afsluiten van het verbeteroverzicht nav de afgenomen test
			self.ids._ResultNaam.text = str(self.resulttexten[0][5])
			self.ids._MissedRune.text = ""
			self.ids._AssociationMissedRune.text = ""
			self.ids._AdviceMissedRune.text = ""
			self.ids._FavourMissedRune.text = ""
			self.ids._MissedRuneNaam.source = "Pics/logorunistica.png"

			self.manager.current = "menuscreen"
			self.manager.transition = RiseInTransition(duration=1)




