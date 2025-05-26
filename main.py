import flet as ft


def main(page: ft.Page):
    page.title = "Учет расходов"
    page.data = 0

    def add_expence(e):
        amount=float(name2_input.value)
        expence = f"Расход:{name1_unput.value}/Сумма:{name2_input.value}"
        expence_list_area.controls.append(ft.Text(value=expence, size=30))
        page.data += amount
        name1_unput.value = ""
        name2_input.value = ""
        expence_count_text.value = f"Общая сумма расходов {page.data} (сом)"
        page.update()

    title = ft.Text(value="Список расходов", size=33)
    name1_unput = ft.TextField(label="Название расхода")
    name2_input = ft.TextField(label="Сумма расхода")
    add_button = ft.ElevatedButton("Добавить", on_click=add_expence)
    expence_count_text = ft.Text(value=f"Общая сумма расходов {page.data} (сом)", size=28)
    expence_list_area = ft.Column()

    page.add(title, name1_unput, name2_input, add_button, expence_count_text, expence_list_area)

ft.app(main)
