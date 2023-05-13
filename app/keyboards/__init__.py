
class Menu:
    new_subject: str = '➕ Новий предмет'
    my_subjects: str = '📚 Мої предмети'
    my_task: str = '📘 Мої завдання'
    settings: str = '⚙ Налаштування'
    help: str = '💬 Допомога'
    back: str = '◀ Назад'
    notify: str = 'Сповіщення: {}'


class Subject:
    add_task: str = '➕ Додати завдання'
    rates: str = '📊 Успішність'
    edit: str = '📝 Редагувати'
    sort: str = '📂 Сортувати'


class Confirm:
    confirm: str = 'Підтвержую ✔'
    cancel: str = 'Відмінити'


class buttons:
    menu = Menu()
    subject = Subject()
    confirm = Confirm()

