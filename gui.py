from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

import vars

Window.size = (500, 350)


class Base(GridLayout):
    rows = 1
    cols = 2

    def test(self):
        print(self.ids)

    def reset(self):
        print("Resetting!")  # Debug
        text_resets = ['input', 'title', 'genre', 'rating', 'format', 'year', 'runtime', 'plot', 'reviews']

        for label in self.ids:
            if label in text_resets:
                self.ids.get(label).text = ""
                print("Cleared:", label)


class FeedbackBox(Widget):
    _good_color = Color(0, 1, 0, 1)
    _bad_color = Color(1, 0, 0, 1)
    height = NumericProperty(250)
    width = NumericProperty(250)
    y = NumericProperty(100)

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(FeedbackBox, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 1, 0.5)
            self.rect = Rectangle(size=self.size, pos=self.pos)


class UPCInput(TextInput):
    height = NumericProperty(50)
    size_hint = (1, None)
    y = NumericProperty(50)
    hint_text = StringProperty("UPC")


class PublishButton(Button):
    height = NumericProperty(50)
    size_hint = (0.5, None)
    y = NumericProperty(0)
    text = "Publish"


class UpdateButton(Button):
    height = NumericProperty(50)
    size_hint = (0.5, None)
    x = NumericProperty(125)
    text = "Update"


class DataBox(TextInput):
    multiline = False

    def update_title(self):
        vars.data_buffer.update(title=self.text)
        # print(vars.data_buffer)  # Debug

    def update_genre(self):
        vars.data_buffer.update(genre=self.text)

    def update_rating(self):
        vars.data_buffer.update(rating=self.text)

    def update_format(self):
        vars.data_buffer.update(format=self.text)

    def update_year(self):
        vars.data_buffer.update(year=self.text)

    def update_length(self):
        vars.data_buffer.update(length=self.text)

    def update_plot(self):
        vars.data_buffer.update(plot=self.text)

    def update_reviews(self):
        vars.data_buffer.update(reviews=self.text)


class ModeButton(Button):
    background_down = StringProperty("")
    background_normal = StringProperty("")
    background_disabled_down = StringProperty("")
    background_disabled_normal = StringProperty("")
    _enabled_color = [0, 1, 0, 0.5]
    _disabled_color = [1, 0, 0, 0.5]

    def change_colors(self, other):
        if self.background_color != self._enabled_color:
            other_color = other.background_color
            other.background_color = self.background_color
            self.background_color = other_color
            vars.auto_mode = not vars.auto_mode
            # print(vars.auto_mode)  # Debug


class HelpButton(Button):
    text = StringProperty("Help")


class ButtonBar(GridLayout):
    rows = 1
    cols = 3


class ScannerApp(App):
    pass


if __name__ == '__main__':
    ScannerApp().run()
