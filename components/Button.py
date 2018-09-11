import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CButton(CDashComponent):
	def __init__(self, text = 'Button', link = '', style = {}, download = None,
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setButton(text, link, style, download)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setButton(self, text, link, style, download):
		self.__text = text
		self.__value = 0
		if (link == ''):
			if download == None:
				self.setDashRendering(html.A(
					html.Button(
						text,
						name=str(super().getID()),
						style=style,
					),
					id=str(super().getID()),
				))
			else:
				self.setDashRendering(html.A(
					html.Button(
						text,
						name=str(super().getID()),
						style=style,
					),
					id=str(super().getID()),
					download=download,
				))

		else:
			if download == None:
				self.setDashRendering(html.A(
					html.Button(
						text,
						style=style,
					),
					id=str(super().getID()),
					href=link,
				))
			else:
				self.setDashRendering(html.A(
					html.Button(
						text,
						style=style,
					),
					id=str(super().getID()),
					href=link,
					download=download,
				))