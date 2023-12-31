
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        #super().__init__(self, **kwargs)
        #print(" INIT W " + str(self.width) + " H " + str(self.height))

    def on_parent(self, widget, parent):
        #print(" On Parent " + str(self.width) + " H " + str(self.height))
        pass

    def on_size(self, *args):
        print(" On Size " + str(self.width) + " H " + str(self.height))









class GalaxyApp(App):
    pass

GalaxyApp().run()