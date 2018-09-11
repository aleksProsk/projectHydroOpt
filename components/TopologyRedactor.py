import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CTopologyRedactor(CDashComponent):
	def __init__(self, types = [], names = [], x = [], y = [], operatesFrom = [], operatesTo = [], style = {},
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setTopologyRedactor(types, names, x, y, operatesFrom, operatesTo, style)
	def setTopologyRedactor(self, types, names, x, y, operatesFrom, operatesTo, style):
		divList = [html.Canvas(id="fabricjs-canvas", style=style)]
		tList = []
		for i in range(len(names)):
			id = "fabricjs-" + types[i] + '-' + names[i] + '-' + str(x[i]) + '-' + str(y[i]) + '-' + operatesFrom[i] + '-' + operatesTo[i]
			tList.append(html.Div(id=id))
		divList.append(html.Div(tList, id="fabricjs-objects-container"))
		self.setDashRendering(html.Div([
            html.Div(divList, id="fabricjs-canvas-container", style=style),
            html.Div([
				'Add Component:',
				html.Button('Reservoir', id="fabricjs-add-reservoir", name="fabricjs-add-reservoir", style={'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '15vw'}),
				html.Button('Turbine', id="fabricjs-add-turbine", name="fabricjs-add-turbine", style={'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '15vw'}),
				html.Button('Pump', id="fabricjs-add-pump", name="fabricjs-add-pump", style={'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '15vw'}),
				html.Button('Flow', id="fabricjs-add-flow", name="fabricjs-add-flow", style={'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '15vw'}),
            ], style={'display': 'flex', 'flexDirection': 'row'}),
			html.Button('Save', id="fabricjs-redactor-save", name="fabricjs-redactor-save", style={'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '15vw'}),
        ], id="fabricjs-redactor"));