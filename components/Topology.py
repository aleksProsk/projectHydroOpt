import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CTopology(CDashComponent):
	def __init__(self, types = [], names = [], x = [], y = [], operatesFrom = [], operatesTo = [], style = {},
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setTopology(types, names, x, y, operatesFrom, operatesTo, style)
	def setTopology(self, types, names, x, y, operatesFrom, operatesTo, style):
		divList = [html.Canvas(id="fabricjs-canvas", style=style)]
		tList = []
		for i in range(len(names)):
			id = "fabricjs-" + types[i] + '-' + names[i] + '-' + str(x[i]) + '-' + str(y[i]) + '-' + operatesFrom[i] + '-' + operatesTo[i]
			tList.append(html.Div(id=id))
		divList.append(html.Div(tList, id="fabricjs-objects-container"))
		self.setDashRendering(html.Div(divList, id="fabricjs-canvas-container", style=style))