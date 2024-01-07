from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')


from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
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

    SPEED_X = 3
    current_offset_x = 0


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        #super().__init__(self, **kwargs)
        #print(" INIT W " + str(self.width) + " H " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()
        Clock.schedule_interval(self.update, 1.0/60.0)


    def on_parent(self, widget, parent):
        #print(" On Parent " + str(self.width) + " H " + str(self.height))
        pass


    def on_size(self, *args):
        #print(" On Size " + str(self.width) + " H " + str(self.height))
        #self.perspective_point_x = self.width/2
        #self.perspective_point_y = self.height * 0.75
        #self.update_vertical_lines()
        #self.update_horizontal_lines()
        pass


    def on_perspective_point_x(self, widget, value):
        #print("PX " + str(value))
        pass

    def on_perspective_point_y(self, widget, value):
        #print("PY " + str(value))
        pass



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


    def transform(self, x, y):

        #return self.transform_2D(x, y)
        return self.transform_perspective(x, y)


    def transform_2D(self, x, y):
        return int(x), int(y)


    def transform_perspective(self, x, y):
        lin_y = y * self.perspective_point_y /self.height

        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y

        diff_x = x-self.perspective_point_x
        diff_y = self.perspective_point_y - lin_y
        factor_y = diff_y / self.perspective_point_y  #1 when diff_y == self.perspective_point_y / 0 when diff_y == 0
        #factor_y = factor_y * factor_y  # same as the next line
        factor_y = pow(factor_y, 4)

        tr_x = self.perspective_point_x + diff_x * factor_y
        tr_y = (1 - factor_y) * self.perspective_point_y

        return int(tr_x), int(tr_y)


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

        self.current_offset_x += self.SPEED_X * time_factor






class GalaxyApp(App):
    pass

GalaxyApp().run()