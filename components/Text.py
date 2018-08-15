import infix
import dash_html_components as html

@infix.div_infix
def m(f, x): return list(map(f, x))

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CText(CDashComponent):
    def __init__(self, text, style = {}, name=None, screenName=None):
        super().__init__(name, screenName)
        self.__style = style
        self.update(text)
    def getText(self): return self.__text
    def update(self, text):
        self.__text = text
        super().setDashRendering(html.P(str(text), className='text', id=str(super().getID()), style=self.__style))

class CNumber(CText):
    def __init__(self, value, unit, name=None, screenName=None):
        super().__init__(str(value) + " " + unit, name=name, screenName=screenName)
        self.__value = value
        self.__unit = unit
        self.update(value, unit)
    def getValue(self): return self.__value
    def update(self, value, unit=None):
        if unit is None: unit = self.__unit
        super().update(str(value) + " " + unit)
        self.__value = value
        self.__unit = unit

class CNumbers(CText):
    def __init__(self, keys_values_units, separator='│', name=None, screenName=None):
        self.__keys_values_units = keys_values_units
        self.__separator = separator
        super().__init__(self._getText(), name=name, screenName=screenName)
    def _getText(self): return (' ' + self.__separator + ' ').join(
        (lambda x: x[0] + ': ' + str(x[1]) + ' ' + x[2]) / m / self.__keys_values_units)
