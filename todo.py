import flet as ft
import sqlite3

class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.WHITE
        self.page.window_width = 450
        self.page.window_height = 450
        self.page.window_resizable = True
        self.page.window_always_on_top = False
        self.page.title = 'ToDo Axis'
        
        

        self.task = ''
        self.view = 'all'
        self.db_execute('CREATE TABLE IF NOT EXISTS tasks(name, status)')
        self.results = self.db_execute('SELECT * FROM tasks')
        self.tabs = None
        self.main_page()
        self.page.window_center()

    def db_execute(self, query, params=[]):
        with sqlite3.connect('tododb.db') as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit() 
            return cur.fetchall()   

    def checked(self, e):
        is_checked = e.control.value
        label = e.control.label

        if is_checked:
            self.db_execute('UPDATE tasks SET status = "complete" WHERE name = ?', params=[label])
        else:
            self.db_execute('UPDATE tasks SET status = "incomplete" WHERE name = ?', params=[label])    

        self.update_tabs()
        self.update_task_list()

    def delete_task(self, task_name):
        self.db_execute('DELETE FROM tasks WHERE name = ?', params=[task_name])
        self.update_tabs()
        self.update_task_list()

    def get_task_counts(self):
        all_count = len(self.db_execute('SELECT * FROM tasks'))
        incomplete_count = len(self.db_execute('SELECT * FROM tasks WHERE status = "incomplete"'))
        complete_count = len(self.db_execute('SELECT * FROM tasks WHERE status = "complete"'))
        return all_count, incomplete_count, complete_count

    def update_tabs(self):
        all_count, incomplete_count, complete_count = self.get_task_counts()
        self.tabs.tabs[0].text = f'Todas tarefas ({all_count})'
        self.tabs.tabs[1].text = f'Em andamento ({incomplete_count})'
        self.tabs.tabs[2].text = f'Finalizados ({complete_count})'
        self.page.update()

    def tasks_container(self):
        return ft.Container(
            height=self.page.height * 0.8,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Checkbox(
                                label=res[0],
                                on_change=self.checked,
                                value=True if res[1] == 'complete' else False
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda e, task=res[0]: self.delete_task(task),
                                tooltip="Excluir tarefa"
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                    for res in self.results if res
                ]
            )
        )

    def set_value(self, e):
        self.task = e.control.value

    def add(self, e, input_task):
        name = self.task
        status = 'incomplete'

        if name:
            self.db_execute(query='INSERT INTO tasks VALUES(?, ?)', params=[name, status])
            input_task.value = ''
            self.update_tabs()
            self.update_task_list()

    def update_task_list(self):
        self.results = self.db_execute('SELECT * FROM tasks') if self.view == 'all' else self.db_execute('SELECT * FROM tasks WHERE status = ?', params=[self.view])
        tasks = self.tasks_container()
        self.page.controls[-1] = tasks
        self.page.update()

    def tabs_changed(self, e):
        if e.control.selected_index == 0:
            self.results = self.db_execute('SELECT * FROM tasks') 
            self.view = 'all'
        elif e.control.selected_index == 1:
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = "incomplete"')
            self.view = 'incomplete'
        elif e.control.selected_index == 2:
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = "complete"')
            self.view = 'complete'

        self.update_task_list()    

    def main_page(self): 
        input_task = ft.TextField(
            hint_text='Digite uma tarefa',
            expand=True,
            on_change=self.set_value) 

        input_bar = ft.Row(
            controls=[
                input_task,
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    on_click=lambda e: self.add(e, input_task))
            ]
        )

        all_count, incomplete_count, complete_count = self.get_task_counts()

        self.tabs = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text=f'Todas tarefas ({all_count})'),
                ft.Tab(text=f'Em andamento ({incomplete_count})'),
                ft.Tab(text=f'Finalizados ({complete_count})')
            ]
        )

        tasks = self.tasks_container()

        self.page.add(input_bar, self.tabs, tasks)
    

# ft.app(target=ToDo, view=ft.WEB_BROWSER) 
ft.app(target=ToDo)
