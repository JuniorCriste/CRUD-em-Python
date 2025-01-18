import flet as ft

class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.WHITE
        self.page.window_width = 380
        self.page.window_height = 450
        self.page.window_resizable = True
        self.page.window_always_on_top = False
        self.page.title = 'ToDo Axis' 
        self.main_page()

    def tasks_container(self):
        return ft.Container(
            height=self.page.height *0.8,
            content=ft.Column(
                controls=[
                    ft.Checkbox(label='Atividade 1', value =True)
                ]
            )
        )    

    def main_page(self): 
        input_task = ft.TextField(hint_text='Digite uma tarefa', expand=True) 

        input_bar = ft.Row(
            controls=[
                input_task,
                ft.FloatingActionButton(icon=ft.icons.ADD)
            ]
        )

        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text='Todas tarefas'),
                ft.Tab(text='Em andamento'),
                ft.Tab(text='Finalizados')
            ]
        )

        tasks = self.tasks_container()

        self.page.add(input_bar, tabs, tasks)

ft.app(target = ToDo)

        