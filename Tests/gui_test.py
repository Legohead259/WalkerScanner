from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from Tests.test_vars import auto


class Marvel(BoxLayout):
    def hulk_smash(self):
        self.ids.hulk.text = "hulk: puny god!"
        self.ids["loki"].text = "loki: >_<!!!"  # alternative syntax
        print(self.ids)


class Hulk(Button):
    def hulk_smash(self):
        print(self.root.ids)
        self.parent.ids.hulk.text = "hulk: puny god!"
        self.parent.ids["loki"].text = "loki: >_<!!!"  # alternative syntax

    def on_auto_change(self):
        print("Auto change detected!")


class TestApp(App):
    pass


if __name__ == '__main__':
    TestApp().run()
