from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class MainLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.cols = 2
        self.rows = 6
        self.spacing = [10, 10]
        self.padding = [10, 10, 10, 0]

        with self.canvas.before:
            self.bg_color = Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=Window.size)

        self.logo = Image(source="logo.png", size_hint=(0.8, 0.8))
        self.add_widget(self.logo)

        self.heading_label = Label(
            text="Project Kriti", font_size=50, color=(1, 0, 0, 1)
        )
        self.add_widget(self.heading_label)

        self.enter_detector_button = Button(
            text="Enter Detector",
            size_hint=(0.6, 0.2),
            background_color=[0, 0.596, 0.859, 1],
            color=[1, 1, 1, 1],
        )
        self.add_widget(self.enter_detector_button)

        self.save_face_button = Button(
            text="Save New Face",
            size_hint=(0.6, 0.2),
            background_color=[0.18, 0.773, 0.443, 1],
            color=[1, 1, 1, 1],
        )
        self.add_widget(self.save_face_button)

        self.ocr_button = Button(
            text="OCR",
            size_hint=(0.6, 0.2),
            background_color=[0.945, 0.769, 0.059, 1],
            color=[1, 1, 1, 1],
        )
        self.add_widget(self.ocr_button)

        self.credits_button = Button(
            text="Credits & More",
            size_hint=(0.6, 0.2),
            background_color=[0.906, 0.298, 0.235, 1],
            color=[1, 1, 1, 1],
        )
        self.add_widget(self.credits_button)

        self.footer_label = Label(
            text="A Project By WS And BS",
            font_size=30,
            color=[1, 1, 1, 1],
            size_hint=(1, 0.2),
            valign="middle",
        )
        self.add_widget(self.footer_label)


class ProjectKritiApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    ProjectKritiApp().run()
