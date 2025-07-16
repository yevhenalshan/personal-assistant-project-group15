

## Структура проєкту

- models/ — класи для роботи з контактами та нотатками
- services/ — логіка роботи з адресною книгою, командами, винятки
- storage.py — збереження/завантаження контактів та нотаток
- birthday.py — пошук майбутніх днів народження
- parser.py — розбір введених команд
- cli.py — командний інтерфейс користувача
- main.py — точка входу
- user_data/ — файли збереження (`addressbook.pkl`, `notes.pkl`)

## Основні класи

- **Field, Name, Phone, Birthday, Record** (models/contact.py): описують контакт та його поля
- **Note** (models/note.py): описує нотатку
- **AddressBook** (services/address_book.py): колекція контактів
- **Exception-класи** (services/exceptions.py): обробка помилок

## Як запустити

1. Встановити залежності:
    ```
    pip install -r requirements.txt
    ```
2. Запустити програму:
    ```
    python main.py
    ```

## Залежності

- Python 3.10+
- colorama (для кольорового тексту в терміналі)

## Команди

- `add [name] [phone]` — додати контакт
- `change [name] [old_phone] [new_phone]` — змінити номер
- `phone [name]` — показати контакт
- `add-birthday [name] [DD.MM.YYYY]` — додати ДН
- `change-birthday [name] [DD.MM.YYYY]` — змінити ДН
- `show-birthday [name]` — показати ДН
- `birthdays` — показати дні народження за тиждень
- `all` — всі контакти
- `help` — список команд
- `exit`/`close` — вийти

## Де зберігаються дані?

Усі дані контактуються у файлах:

user_data/addressbook.pkl # контакти та дні народження
user_data/notes.pkl # нотатки