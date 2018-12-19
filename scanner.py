from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

import vars
from util import query_ombd

Window.size = (500, 350)


class Base(GridLayout):
    def test(self):
        print(self.ids)

    def reset(self):
        # print("Resetting...")  # Debug
        fields = ['input', 'title', 'genre', 'rating', 'format', 'year', 'runtime', 'plot', 'reviews']

        for label in self.ids:
            if label in fields:
                self.ids.get(label).text = ""
                # print("Cleared:", label)  # Debug

        self.ids['feedback'].set_standby()

    def update(self):
        # print("Updating...")  # Debug
        fields = ['title', 'genre', 'rating', 'format', 'year', 'runtime', 'plot', 'reviews']

        for label in self.ids:
            if label in fields:
                try:
                    self.ids.get(label).text = vars.data_buffer[label]
                    # print("Updated:", label)  # Debug
                except KeyError:
                    pass


class FeedbackBox(Widget):
    _good_color = [0, 1, 0, 0.5]
    _bad_color = [1, 0, 0, 0.5]
    _standby_color = [0, 0, 1, 0.5]
    active_color = ListProperty()
    rect = None

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(FeedbackBox, self).__init__(**kwargs)
        self.active_color = self._standby_color

    def set_good(self):
        # print("Setting GOOD color...")  # Debug
        self.active_color = self._good_color

    def set_bad(self):
        # print("Setting BAD color...")  # Debug
        self.active_color = self._bad_color

    def set_standby(self):
        # print("Setting STANDBY color...")  # Debug
        self.active_color = self._standby_color


class UPCInput(TextInput):
    pass


class PublishButton(Button):
    pass


class ResetButton(Button):
    pass


class DataBox(TextInput):
    def update_title(self):
        # print("Querying...")  # Debug
        if query_ombd(self.text):
            root.update()
            root.ids['feedback'].set_good()
        else:
            root.ids['feedback'].set_bad()

        # print(vars.auto_mode)  # Debug
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


class HelpButton(Button):
    pass


class ButtonBar(GridLayout):
    pass


class ScannerApp(App):
    def build(self):
        global root
        root = Base()
        return root


if __name__ == '__main__':
    ScannerApp().run()
