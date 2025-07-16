from datetime import datetime
from models.note import Note

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
        if not phone.isdigit():
            raise ValueError("Phone number must consist of digits.")
        elif len(phone) != 10:
            raise ValueError("Phone number must consist of 10 digits.")
        else:
            super().__init__(phone)

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
        self.notes = []

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def change_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)
        print(f"Birthday date updated.")

    def add_phone(self, phone: str) -> None:
        if self.find_phone(phone):
            from services.exceptions import PhoneAlreadyExistsError
            raise PhoneAlreadyExistsError(self.name)
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
        if old_phone_obj:
            self.phones.remove(old_phone_obj)
            new_phone_obj = Phone(new_phone)
            self.phones.append(new_phone_obj)
        else:
            raise ValueError("Phone number not found.")

    def find_phone(self, phone: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        if self.phones:
            return f"Contact name: {str(self.name).capitalize()}, phones: {'; '.join(p.value for p in self.phones)}"
        return f"There are no phones in {str(self.name).capitalize()}'s record"
