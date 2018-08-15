log.print("starting renderer")

myScreen = CPage('Assets')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

return myScreen


