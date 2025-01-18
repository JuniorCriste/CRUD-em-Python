import flet as ft

class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.WHITE
        self.page.window_width = 200
        self.page.window_height = 200
        self.page.window_resizable = True
        self.page.window_always_on_top = False
        self.page.title = 'ToDo Axis' 
        self.main_page()

    def main_page(self): 
        input_task = ft.TextField(hint_text='Digite uma tarefa', expand=True) 

        input_bar = ft.Row(
            controls=[
                input_task,
                ft.FloatingActionButton(icon=ft.icons.ADD)
            ]
        )

        self.page.add(input_bar)

ft.app(target = ToDo)

        