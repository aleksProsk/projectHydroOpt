import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CYMap(CDashComponent):
    def __init__(self, names = [], lat = [], lon = [], draggable = [], style = {},
                 name = None, screenName = None):
        super().__init__(name, screenName)
        self.setYMap(names, lat, lon, draggable, style, 0)
    def setYMap(self, names, lat, lon, draggable, style, fakeContainers):
        divList = [html.Div(id="ymap-container", style=style)]
        divPlacemarks = []
        for i in range(len(names)):
            id = "ymapsmark-"+names[i]+'-'+str(lat[i])+'-'+str(lon[i])
            if draggable[i] == True:
                id = id + '-draggable'
            divPlacemarks.append(html.Div(id=id))
        for i in range(fakeContainers):
            divPlacemarks.append(html.Div())
        divList.append(html.Div(divPlacemarks, id="ymap-placemarks-container"))
        self.__content = divList
        self.setDashRendering(html.Div(divList, id=str(super().getID())))
    def getContent(self): return self.__content