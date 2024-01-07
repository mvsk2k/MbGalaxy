from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window

from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):

    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_keyboard_up, on_keyboard_down, on_touch_down, on_touch_up, keyboard_closed
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    #line = None

    V_NB_LINES = 10
    V_LINES_SPACING = 0.25  #Percentage in screen width
    vertical_lines = []

    H_NB_LINES = 15
    H_LINES_SPACING = 0.1  # Percentage in screen Height
    horizontal_lines = []
    SPEED = 4

    current_offset_y = 0

    SPEED_X = 12
    current_speed_x = 0
    current_offset_x = 0


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        #super().__init__(self, **kwargs)
        #print(" INIT W " + str(self.width) + " H " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0/60.0)

    def is_desktop(self):
        if platform in ("linux", "win", "macosx"):
            return True
        return False


    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            #self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def update_vertical_lines(self):
        #center_x = int(self.width/2)
        #self.line.points = [center_x, 0, center_x, 100]

        center_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        #offset = -int(self.V_NB_LINES/2)
        offset = -int(self.V_NB_LINES / 2) + 0.5     # to center the space

        for i in range(0, self.V_NB_LINES):
            line_x = int(center_line_x + offset * spacing + self.current_offset_x)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            #self.vertical_lines[i].points = [line_x, 0, line_x, self.height]
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1


    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):

        center_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        offset = int(self.V_NB_LINES / 2) - 0.5  # to center the space

        xmin = center_line_x - offset * spacing + self.current_offset_x
        xmax = center_line_x + offset * spacing + self.current_offset_x
        spacing_y = self.H_LINES_SPACING * self.height

        for i in range(0, self.H_NB_LINES):
            line_y = i * spacing_y - self.current_offset_y
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]




    def update (self, dt):
        # print("Update")
        #print("dt:" + str(dt) + " - 1/60: " + str(1.0/60.0))
       #print("dt:" + str(dt*60))
        time_factor = dt*60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.SPEED * time_factor

        spacing_y = self.H_LINES_SPACING * self.height

        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

        self.current_offset_x += self.current_speed_x * time_factor



class GalaxyApp(App):
    pass

GalaxyApp().run()