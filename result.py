import sqlite3
import time
from kivy.properties import StringProperty, NumericProperty,ListProperty
from kivy.uix.screenmanager import Screen, WipeTransition, RiseInTransition


class ResultScreen(Screen):

	Score_quizz = NumericProperty()
	Missed_questions = ListProperty([])
	teller = NumericProperty()
	tel=NumericProperty()
	indicator = StringProperty("")

	def CleanUp(self, *args):

		self.teller= 0
		self.Missed_quistions=[]
		self.Score_quizz = 0
		self.tel=0
		self.indicator= ""

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
		else:
			self.Missed_quistions = []

		if len(self.Missed_quistions) > 0:
			pass

		else:
			pass

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
			self.ids._ResultNaam.text = ""
			self.ids._MissedRune.text = str(self.DisplaySelection[self.tel][0][0])
			self.ids._MissedRuneNaam.source= "Tekens/"+ (str(self.DisplaySelection[self.tel][0][0])).lower()+".png"
			self.ids._AssociationMissedRune.text = f"This rune is associated with:\n {self.DisplaySelection[self.tel][0][1]}"
			self.ids._AdviceMissedRune.text = f"Message or advice of this rune:\n {self.DisplaySelection[self.tel][0][2]}"
			self.ids._FavourMissedRune.text = f"This rune is considered:\n {self.DisplaySelection[self.tel][0][3]}"
			self.ids._ButtonAdvice.text = "<< Next Advice>>"
			self.tel += next

		else:
			self.ids._ResultNaam.text = "End of summarizing\n the runes to study"
			self.ids._MissedRune.text = ""
			self.ids._AssociationMissedRune.text = ""
			self.ids._AdviceMissedRune.text = ""
			self.ids._FavourMissedRune.text = ""
			self.ids._MissedRuneNaam.source = "Pics/logorunistica.png"
			self.manager.current = "menuscreen"
			self.manager.transition = RiseInTransition(duration=1)




