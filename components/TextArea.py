import dash_core_components as dcc

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CTextArea(CDashComponent):
	def __init__(self, cols = 20, contentEditable = True, disabled = False, draggable = False, maxLength = -1, minLength = -1,
				 placeholder = 'Enter text', readonly = False, rows = 20, style = {}, title = '', value = None,
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setTextArea(cols, contentEditable, disabled, draggable, maxLength, minLength, placeholder, readonly, rows, style, title, value)
	def update(self, value):
		self.__value = value
	def getValue(self):
		return self.__value
	def setTextArea(self, cols, contentEditable, disabled, draggable, maxLength, minLength, placeholder, readonly, rows, style,title, value):
		self.__cols = cols
		self.__rows = rows
		self.__value = value
		super().setDashRendering(dcc.Textarea(
			id=str(super().getID()),
			name=str(super().getID()),
			cols=cols,
			contentEditable=contentEditable,
			disabled=disabled,
			draggable=draggable,
			maxLength=maxLength,
			minLength=minLength,
			placeholder=placeholder,
			readOnly=readonly,
			rows=rows,
			title=title,
			value=value,
			style=style,
		))