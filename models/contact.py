from services.exceptions import PhoneAlreadyExistsError
from datetime import datetime
import re

class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

class Name(Field):
    def __init__(self, name: str) -> None:
        if not name.isalpha():
            raise ValueError("Name must be alphabetic")
        super().__init__(name.casefold())

    def __eq__(self, other) -> bool:
        return isinstance(other, Name) and self.value == other.value

    def __str__(self) -> str:
        return self.value

class Phone(Field):
    def __init__(self, phone) -> None:
        match_phone = re.fullmatch(r"\+?\d{10,15}", phone)
        if match_phone:
            super().__init__(phone)
        else:
            raise ValueError("Phone number is either too short, too long or uses invalid format. Use 'help' for additional info") #TODO: в 'help' треба описати правильний формат, наприклад: +38(050)123-32-34, або просто 1234567890

    def __eq__(self, other) -> bool:
        if isinstance(other, Phone) and self.value == other.value:
            return True
        return NotImplemented

    def __str__(self) -> str:
        return self.value

class Birthday(Field):
    def __init__(self, value) -> None:
        try:
            self.birthday = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value

class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.note = None
    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def change_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)
        print(f"Birthday date updated.")

    def add_phone(self, phone: str) -> None:
        if self.find_phone(phone):
            raise PhoneAlreadyExistsError(self.name.value)
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone: str) -> None:
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError("Phone number not found.")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        old_phone_obj = self.find_phone(old_phone)
        new_phone_exists = self.find_phone(new_phone)

        if not old_phone_obj:
            raise ValueError("Phone number not found.")
        elif new_phone_exists:
            raise PhoneAlreadyExistsError(self.name.value)
        else:
            self.phones.remove(old_phone_obj)
            new_phone_obj = Phone(new_phone)
            self.phones.append(new_phone_obj)

    def find_phone(self, phone: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_note(self, title: str, text: str, tags: list[str] = None) -> None:
        note = Note(title, text, tags or [])
        self.note = note

    def remove_note(self) -> None:
        if self.note:
            self.note = None
        else:
            raise ValueError("No note to remove.")

    def edit_note(self, title: str, text: str, tags: list[str] = None) -> None:
        if self.note:
            self.note.title = title
            self.note.text = text
            if tags is not None:
                self.note.tags = tags
        else:
            raise ValueError("No note to edit.")
    
    def __str__(self) -> str:
        if self.phones:
            return f"Contact name: {str(self.name).capitalize()}, phones: {'; '.join(p.value for p in self.phones)}"
        return f"There are no phones in {str(self.name).capitalize()}'s record"

class Note(Field):
    def __init__(self, title: str, text: str, tags: list[str] = None) -> None:
        if not title.strip():
            raise ValueError("Note title cannot be empty.")
        self.title = title.strip()
        self.text = text.strip()
        self.tags = tags or []

    def __str__(self) -> str:
        tags_str = f" [Tags: {', '.join(self.tags)}]" if self.tags else ""
        return f"Note: {self.title}: {self.text}{tags_str}"

