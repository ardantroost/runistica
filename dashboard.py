import sqlite3
from random import random
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from plyer import tts
from kivy_garden.mapview import MapView, MapMarker


class DashboardScreen(Screen):

	def mapviewer(self):

		#layer = ClusteredMarkerLayer()
		#for i in range(20):
		#	lon = random() * 360 - 180
		#	lat = random() * 180 - 90
		#	layer.add_marker(lon=lon, lat=lat, cls=MapMarker)

		# then you can add the layer to your mapview

		#mapview = MapView()
		#mapview.add_widget(layer)

		mapview = MapView(lat=52.059386, lon=5.289238,zoom=12)

		self.add_widget(mapview)
		mapview.add_widget(MapMarker(lat=52.059386, lon=5.289238))
		mapview.add_widget(MapMarker(lat=52.091443, lon=5.245218))
		mapview.add_widget(MapMarker(lat=52.048109, lon=5.265666))

	def on_enter(self):

		conn= sqlite3.connect("rdatabase.db")
		c=conn.cursor()
		c.execute("""CREATE TABLE IF NOT EXISTS runenstatistics (
			naam text,
			lastvist text,
			score_tekens real,
			score_symbols real,
			score_meaning real)
			""")
		c.execute("SELECT * FROM runenstatistics")
		items= c. fetchall()
		print(str(items))
		conn.commit()
		conn.close()

		self.mapviewer()




