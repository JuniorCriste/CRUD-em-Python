import flet as ft

class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.YELLOW
        self.page.window.width = 200
        self.page.window.height = 200
        self.page.window_resizable = False
        self.page.window_always_on_top
        self.page.title = 'ToDo Axis'
        self.main_page()

    def main_page(self):
        pass

ft.app(target=ToDo)
        