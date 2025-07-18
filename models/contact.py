from services.exceptions import PhoneAlreadyExistsError, EmailAlreadyExistsError
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
        super().__init__(name.casefold().capitalize())

    def __eq__(self, other) -> bool:
        return isinstance(other, Name) and self.value == other.value

    def __str__(self) -> str:
        return self.value

class Phone(Field):
    def __init__(self, phone: str) -> None:
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
    def __init__(self, birthday: str) -> None:
        try:
            self.birthday = datetime.strptime(birthday, "%d.%m.%Y")
            super().__init__(birthday)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value
    
class Email(Field):
    def __init__(self, email: str) -> None:
        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if valid_email:
            super().__init__(email)
        else:
            raise ValueError("Email is in incorrect format.")
    
    def __str__(self) -> str:
        return self.value
    
class Address(Field):
    def __init__(self, address: str) -> None:
        super().__init__(address.title())
    
    def __str__(self) -> str:
        return self.value

class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.address = None
        self.note = None
      
    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def change_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

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

    def change_phone(self, old_phone: str, new_phone: str) -> None:
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
    

    def add_note(self, title: str, text: str, tags: list[str] | None = None) -> None:
        note = Note(title, text, tags or [])
        self.note = note

    def add_email(self, email: str) -> None:
        if self.find_email(email):
            raise EmailAlreadyExistsError(self.name.value)
        self.emails.append(Email(email))

    def change_email(self, old_email: str, new_email: str) -> None:
        old_email_obj = self.find_phone(old_email)
        new_email_obj = self.find_phone(new_email)

        if not old_email_obj:
            raise ValueError("Email not found.")
        elif new_email_obj:
            raise EmailAlreadyExistsError(self.name.value)
        else:
            self.emails.remove(old_email_obj)
            new_email_obj = Email(new_email)
            self.phones.append(new_email_obj)

    def remove_email(self, email: str) -> None:
        email_obj = self.find_email(email)
        if email_obj is None:
            raise ValueError("Email not found.")
        else:
            self.emails.remove(email_obj)

    def find_email(self, email: str) -> Email | None:
        for el in self.emails:
            if el.value == email:
                return el
        return None
    
    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def change_address(self, address: str) -> None:
        self.address = Address(address)

    def remove_note(self) -> None:
        if self.note:
            self.note = None
        else:
            raise ValueError("No note to remove.")

    def edit_note(self, title: str, text: str, tags: list[str] | None = None) -> None:
        if self.note:
            self.note.title = title
            self.note.text = text
            if tags is not None:
                self.note.tags = tags
        else:
            raise ValueError("No note to edit.")
    
    def __str__(self) -> str:
        result = f"Contact name: {str(self.name).capitalize()}"
        
        if self.phones:
            result += f", phones: {'; '.join(p.value for p in self.phones)}"
        else:
            result += f" (no phones)"
            
        if self.note:
            result += f" | Note: {self.note.title}: {self.note.text}"
            if self.note.tags:
                result += f" [Tags: {', '.join(self.note.tags)}]"
                
        return result

class Note(Field):
    def __init__(self, title: str, text: str, tags: list[str] | None = None) -> None:
        if not title.strip():
            raise ValueError("Note title cannot be empty.")
        self.title = title.strip()
        self.text = text.strip()
        self.tags = tags or []

    def __str__(self) -> str:
        tags_str = f" [Tags: {', '.join(self.tags)}]" if self.tags else ""
        return f"Note: {self.title}: {self.text}{tags_str}"

