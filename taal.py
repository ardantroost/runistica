import sqlite3
from kivy.properties import StringProperty, ListProperty

lanquage = StringProperty("")
page_menu = ListProperty([])


def translate_menu(self,menu):

	self.page_one = menu[0]
	self.screens[1].ids._page1header.text = self.page_one[0]
	self.screens[1].ids._label_testrunes.text = self.page_one[2]
	self.screens[1].ids._label_testnames.text = self.page_one[3]
	self.screens[1].ids._label_testmeaning.text = self.page_one[4]

	self.screens[1].ids._Header_college.text = self.page_one[1]
	self.screens[1].ids._label_library.text = self.page_one[5]
	self.screens[1].ids._label_practicum.text = self.page_one[6]
	self.screens[1].ids._label_personaladvice.text = self.page_one[7]

	self.screens[1].ids._ButtonStart.text = self.page_one[8]

def translate_vragen(self,vragen):

	self.page_vragen = vragen[0]

	self.screens[3].ids._Header_testsymbol.text = self.page_vragen[0]
	self.screens[3].ids._label_vraag.text = self.page_vragen[1]
	self.screens[3].ids._button_start.text = self.page_vragen[2]

def translate_vrageneen(self, page_vrageneen):

	self.page_vrageneen = page_vrageneen[0]

	self.screens[4].ids._header.text = self.page_vrageneen[0]
	self.screens[4].ids._label_vraag.text = self.page_vrageneen[1]
	self.screens[4].ids._button_start.text = self.page_vrageneen[2]

def translate_vragentwee(self, page_vragentwee):

	self.page_vragentwee = page_vragentwee[0]

	self.screens[5].ids._header.text = self.page_vragentwee[0]
	self.screens[5].ids._label_vraag.text = self.page_vragentwee[1]
	self.screens[5].ids._button_start.text = self.page_vragentwee[2]


def translate_stats(self, page_stats):

	self.page_stats = page_stats[0]

	self.screens[9].ids._header.text = self.page_stats[0]
	self.screens[9].ids._current.text = self.page_stats[1]
	self.screens[9].ids._skill_runes.text = self.page_stats[2]
	self.screens[9].ids._skill_names.text = self.page_stats[3]
	self.screens[9].ids._skill_meaning.text = self.page_stats[4]

	self.screens[9].ids._stat_runes_header.text = self.page_stats[5]
	self.screens[9].ids._stat_runes_final.text = self.page_stats[6]
	self.screens[9].ids._stat_runes_lasttest.text = self.page_stats[7]
	self.screens[9].ids._stat_runes_date.text = self.page_stats[8]

	self.screens[9].ids._stat_names_header.text = self.page_stats[9]
	self.screens[9].ids._stat_names_final.text = self.page_stats[10]
	self.screens[9].ids._stat_names_lasttest.text = self.page_stats[11]
	self.screens[9].ids._stat_names_date.text = self.page_stats[12]

	self.screens[9].ids._stat_meaning_header.text = self.page_stats[13]
	self.screens[9].ids._stat_meaning_final.text = self.page_stats[14]
	self.screens[9].ids._stat_meaning_lasttest.text = self.page_stats[15]
	self.screens[9].ids._stat_meaning_date.text = self.page_stats[16]
	self.screens[9].ids._swipe.text = self.page_stats[17]

def translate_collegesymbols(self,page_collegesymbols):

	self.page_collegesymbols = page_collegesymbols[0]
	self.screens[7].ids._header.text = self.page_collegesymbols[0]
	self.screens[7].ids._label_association.text = self.page_collegesymbols[1]
	self.screens[7].ids._label_interpretation.text = self.page_collegesymbols[2]

def translate_collegenames(self,page_collegenames):

	self.page_collegenames = page_collegenames[0]
	self.screens[8].ids._header.text = self.page_collegenames[0]
	self.screens[8].ids._Buttoncheck.text = self.page_collegenames[1]
	self.screens[8].ids._Buttoncheck.taal = self.page_collegenames[2]

def taalknop(self,speak):

	self.lanquage = speak
	conn = sqlite3.connect("taalkeuze.db")
	c = conn.cursor()

	if self.lanquage == 'Engels':
		c.execute("SELECT Headertest_eng, Headercollege_eng, testeng_symbol,testeng_names, testeng_meaning, "
				  "collegeeng_library , collegeeng_prakticum,collegeeng_personaladvice,choose_eng FROM menu")
		menu = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vragen WHERE taal=(?)",("Engels",))
		page_vragen = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vrageneen WHERE taal=(?)", ("Engels",))
		page_vrageneen = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vragentwee WHERE taal=(?)", ("Engels",))
		page_vragentwee = c.fetchall()
		c.execute("SELECT header, current, skillrunes, skillnames, skillmeaning, statrunesheader, statrunesfinal, statruneslasttest, statrunesdate, statnamesheader, statnamesfinal, statnameslasttest, statnamesdate, statmeaningheader, statmeaningfinal, statmeaninglasttest, statmeaningdate, swipe FROM stats WHERE taal=(?)", ("Engels",))
		page_stats = c.fetchall()
		c.execute("SELECT header, association, interpretation FROM collegesymbols WHERE taal=(?)", ("Engels",))
		page_collegesymbols = c.fetchall()
		c.execute("SELECT header, button, button2 FROM collegenames WHERE taal=(?)", ("Engels",))
		page_collegenames = c.fetchall()

	elif self.lanquage == 'Frans':
		c.execute("SELECT Headertest_fr, Headercollege_fr, testfr_symbol,testfr_names, testfr_meaning, "
				  "collegefr_library , collegefr_prakticum,collegefr_personaladvice, choose_fr FROM menu")
		menu = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vragen WHERE taal=(?)", ("Frans",))
		page_vragen = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vrageneen WHERE taal=(?)", ("Frans",))
		page_vrageneen = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vragentwee WHERE taal=(?)", ("Frans",))
		page_vragentwee = c.fetchall()
		c.execute("SELECT header, current, skillrunes, skillnames, skillmeaning, statrunesheader, statrunesfinal, statruneslasttest, statrunesdate, statnamesheader, statnamesfinal, statnameslasttest, statnamesdate, statmeaningheader, statmeaningfinal, statmeaninglasttest, statmeaningdate,swipe FROM stats WHERE taal=(?)", ("Frans",))
		page_stats = c.fetchall()
		c.execute("SELECT header, association, interpretation FROM collegesymbols WHERE taal=(?)", ("Frans",))
		page_collegesymbols = c.fetchall()
		c.execute("SELECT header, button, button2 FROM collegenames WHERE taal=(?)", ("Frans",))
		page_collegenames = c.fetchall()

	elif self.lanquage == 'Duits':
		c.execute("SELECT Headertest_dts, Headercollege_dts, testdts_symbol,testdts_names, testdts_meaning, "
				  "collegedts_library , collegedts_prakticum,collegedts_personaladvice,choose_dts FROM menu")
		menu = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vragen WHERE taal=(?)", ("Duits",))
		page_vragen = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vrageneen WHERE taal=(?)", ("Duits",))
		page_vrageneen = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vragentwee WHERE taal=(?)", ("Duits",))
		page_vragentwee = c.fetchall()
		c.execute("SELECT header, current, skillrunes, skillnames, skillmeaning, statrunesheader, statrunesfinal, statruneslasttest, statrunesdate, statnamesheader, statnamesfinal, statnameslasttest, statnamesdate, statmeaningheader, statmeaningfinal, statmeaninglasttest, statmeaningdate,swipe FROM stats WHERE taal=(?)", ("Duits",))
		page_stats = c.fetchall()
		c.execute("SELECT header, association, interpretation FROM collegesymbols WHERE taal=(?)", ("Duits",))
		page_collegesymbols = c.fetchall()
		c.execute("SELECT header, button, button2 FROM collegenames WHERE taal=(?)", ("Duits",))
		page_collegenames = c.fetchall()

	elif self.lanquage == 'Nederlands':
		c.execute("SELECT Headertest_ned, Headercollege_ned, testned_symbol,testned_names, testned_meaning, "
				  "collegened_library , collegened_prakticum,collegened_personaladvice,choose_ned FROM menu")
		menu = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vragen WHERE taal=(?)", ("Nederlands",))
		page_vragen = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vrageneen WHERE taal=(?)", ("Nederlands",))
		page_vrageneen = c.fetchall()
		c.execute("SELECT header, label_vraag, button_start FROM vragentwee WHERE taal=(?)", ("Duits",))
		page_vragentwee = c.fetchall()
		c.execute("SELECT header, current, skillrunes, skillnames, skillmeaning, statrunesheader, statrunesfinal, statruneslasttest, statrunesdate, statnamesheader, statnamesfinal, statnameslasttest, statnamesdate, statmeaningheader, statmeaningfinal, statmeaninglasttest, statmeaningdate,swipe FROM stats WHERE taal=(?)", ("Nederlands",))
		page_stats = c.fetchall()
		c.execute("SELECT header, association, interpretation FROM collegesymbols WHERE taal=(?)", ("Nederlands",))
		page_collegesymbols = c.fetchall()
		c.execute("SELECT header, button, button2 FROM collegenames WHERE taal=(?)", ("Nederlands",))
		page_collegenames = c.fetchall()

	translate_menu(self,menu)
	translate_vragen(self,page_vragen)
	translate_vrageneen(self,page_vrageneen)
	translate_vragentwee(self,page_vragentwee)
	translate_stats(self, page_stats)
	translate_collegesymbols(self,page_collegesymbols)
	translate_collegenames(self, page_collegenames)


	conn.commit()
	conn.close()

