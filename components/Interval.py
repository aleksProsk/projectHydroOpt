import dash_core_components as dcc

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CInterval(CDashComponent):
	def __init__(self, interval = 1000, name = None, screenName = None):
		super().__init__(name, screenName)
		self.setInterval(interval)
	def update(self, value):
		self.__n_intervals = value
	def getValue(self):
		return self.__n_intervals
	def setInterval(self, interval):
		self.__interval = interval
		super().setDashRendering(dcc.Interval(
			id=str(super().getID()),
			interval=interval,
			n_intervals=0,
		))