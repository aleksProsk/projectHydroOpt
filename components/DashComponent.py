from baseObjects import Restricted

CGUIComponent = Restricted.CGUIComponent

class CDashComponent(CGUIComponent):
	def setDashRendering(self, r): self.__dashRendering = r
	def getDashRendering(self): return self.__dashRendering
	def appendChild(self,c):
		super().appendChild(c)
		self.__dashRendering.children.append(c.getDashRendering())
	def aChild(self,c): self.appendChild(c)