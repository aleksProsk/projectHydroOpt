log.print("starting renderer")

myScreen = CPage('About')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

return myScreen


