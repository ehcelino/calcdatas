import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window

Window.size = (300, 550)

class CDataApp(App):

    def build(self):
        pass
        # return Button(text='Hello World')


if __name__ == '__main__':
    CDataApp().run()