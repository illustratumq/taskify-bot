
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
    skip: str = 'Пропустити'


class EditSubject:
    edit_name: str = 'Редагувати назву'
    edit_max_grade: str = 'Редагувати макс. бал'
    edit_description: str = 'Редагувати опис'
    extra_grade: str = '➕ Додатковий бал'
    delete_subject: str = 'Видалити предмет'


class Sort:
    tags: str = 'По тегам'
    deadline: str = 'По дедлайнам'


class buttons:
    menu = Menu()
    subject = Subject()
    confirm = Confirm()
    edit_subject = EditSubject()
    sort = Sort()


