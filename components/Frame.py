import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CFrame(CDashComponent): #todo: eindeutiger id-parameter
	def __init__(self, sCaption = '', hasCaption = True, type = 'frame', isDynamic = True, width = 0.25, height = 0, smallScreenFactor = 2,
                 tinyScreenFactor = 4, captionType = html.H2, style = {}, name = None, screenName = None):
		super().__init__(name, screenName)
		self.__captionType = captionType
		self.__caption = sCaption
		self.__hasCaption = hasCaption
		self.__width = width
		self.__height = height
		self.__smallScreenFactor = smallScreenFactor
		self.__tinyScreenFactor = tinyScreenFactor
		self.__type = type
		if isDynamic: self.__type = type + ' grid-item varsize' + '-' + str(round(width*100)) + '-' + str(round(height*100)) + '-' + str(round(smallScreenFactor)) + '-' + str(round(tinyScreenFactor))
		self.setCaption(sCaption, hasCaption, style)
	def getCaption(self): return self._caption
	def setCaption(self, sCaption, hasCaption, style = {}):
		children = []
		if hasCaption == True:
			children = [self.__captionType(sCaption, className = 'frame-caption', style={'width': '100%'})]
		super().setDashRendering(html.Div(className = self.__type, children = children, style=style))