import dash_html_components as html

from components import Frame
CFrame = Frame.CFrame

class CPage(CFrame): #todo: eindeutiger id-parameter
	def __init__(self, sCaption, name = None, screenName = None):
		super().__init__(sCaption, type = 'content', isDynamic = False, captionType = html.H1, name = name, screenName = screenName)