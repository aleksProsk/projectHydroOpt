import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CSelectList(CDashComponent):
    def __init__(self, labels = [], containerStyle = {'display': 'flex', 'flex-direction': 'column'}, labelStyle = {'background': 'white', 'color': 'black'},
                 selectedLabelStyle = {'background': 'black', 'color': 'white'}, name = None, screenName = None):
        super().__init__(name, screenName)
        self.__selectedLabels = [0 for i in range(len(labels))]
        self.setSelectList(labels, containerStyle, labelStyle, selectedLabelStyle)
    def setSelectList(self, labels, containerStyle, labelStyle, selectedLabelStyle):
        self.__labels = labels
        self.__containerStyle = containerStyle
        self.__labelStyle = labelStyle
        self.__selectedLabelStyle = selectedLabelStyle
        self.__content = []
        for i in range(len(labels)):
            if self.__selectedLabels[i] == 0:
                self.__content.append(html.Div(labels[i], style=labelStyle, id=super().getID()+'-label-'+str(i)))
            else:
                self.__content.append(html.Div(labels[i], style=selectedLabelStyle, id=super().getID()+'-label-'+str(i)))
        super().setDashRendering(html.Div(self.__content, style=containerStyle, id=super().getID()))
    def setLabels(self, newLabels):
        self.__labels = newLabels
        self.__selectedLabels = [0 in range(len(newLabels))]
        self.setSelectList(newLabels, self.__containerStyle, self.__labelStyle, self.__selectedLabelStyle)
        return super().getDashRendering()
    def getSelected(self):
        return self.__selectedLabels
    def select(self, selectedLabels):
        self.__selectedLabels = selectedLabels
        self.setSelectList(self.__labels, self.__containerStyle, self.__labelStyle, self.__selectedLabelStyle)
        return self.__content