import dash_html_components as html
import infix

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

@infix.div_infix
def m(f,x): return list(map(f,x))

def flatten(lis):
	"""Given a list, possibly nested to any level, return it flattened."""
	new_lis = []
	for item in lis:
		if type(item) == type([]):
			new_lis.extend(flatten(item))
		else:
			new_lis.append(item)
	return new_lis

class CNavigationPane(CDashComponent):
	def __init__(self, nestedLinkList, name = None, screenName = None):
		super().__init__(name, screenName)
		self.setNavigationTree(nestedLinkList)
	def getNavigationTree(self): return self.__nestedLinkList
	def setNavigationTree(self, nestedLinkList):
		self.__nestedLinkList = nestedLinkList
		#nestedLinkList = [['Screens', [['Result overview', 'url'], ['Engine results', 'url']]], ['Assets', [['VSM', 'url'], ['NdD', 'url']]]]
		linkRendering =  flatten((lambda x: [html.P(str(x[0])+': ', className = 'no-break'), (lambda y: html.A(html.Button(y[0], className=y[2]), href=y[1])) /m/ x[1]]) /m/ nestedLinkList)
		super().setDashRendering(html.Div(className = 'navigation-pane', children = linkRendering))