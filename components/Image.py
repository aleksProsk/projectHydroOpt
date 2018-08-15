import dash_html_components as html
import base64

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CImage(CDashComponent):
    def __init__(self, src = '', format = 'png', style = {}, name = 'None', screenName = 'None'):
        super().__init__(name, screenName)
        self.setImage(src, format, style)
    def update(self, value):
        return
    def setImage(self, src, format, style):
        self.__src = src
        #TODO: User is hardcoded!!!
        encoded_image = str(base64.b64encode(open('user001/img/' + src, 'rb').read()))
        self.setDashRendering(html.Img(id=super().getID(), src=('data:image/' + format + ';base64,{}').format(encoded_image[2:-1]), style=style))