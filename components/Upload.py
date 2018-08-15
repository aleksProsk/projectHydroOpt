import dash_core_components as dcc

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

#TODO: Add feature of multiple file upload!!!
class CUpload(CDashComponent):
	def __init__(self, text = 'Drag and Drop or Select a File', max_size = -1, multiple = False, style = {},
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setUpload(text, max_size, multiple, style)
	def getValue(self):
		return [self.__filename, self.__contents]
	def update(self, contents = None, filename = None):
		if contents is not None:
			self.__contents = contents
		if filename is not None:
			self.__filename = filename
	def setUpload(self, text, max_size, multiple, style):
		self.__max_size = max_size
		self.__filename = None
		self.__contents = None
		lineHeight = 'auto'
		super().setDashRendering(dcc.Upload(
			[text],
			id=str(super().getID()),
			max_size=max_size,
			multiple=multiple,
			style=style,
		))