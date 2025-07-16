from services.exceptions import (
    EmptyDictError,
    PhoneAlreadyExistsError,
    BirthdayAlreadyExistsError,
    BirthdayNotSetError
)
from models.contact import Record
from services.address_book import AddressBook
import re

# Декоратор обробки помилок
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(e)
        except KeyError:
            print("Given username was not found in the contact list.")
        except IndexError:
            print("Too few arguments were given. Use 'help' for additional info.")
        except EmptyDictError:
            print("Address book is empty. Add a contact with 'add' command.")
        except (PhoneAlreadyExistsError, BirthdayAlreadyExistsError, BirthdayNotSetError) as e:
            print(e)
    return inner

@input_error
def add_contact(args: list[str], book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexError

    name = args[0]
    phone = "".join(args[1:]) 
    clean_phone = re.sub(r"[^\d+]", "", phone)
    record = book.find(name)

    if not record:
        record_entry = Record(name)
        record_entry.add_phone(clean_phone)
        book.add_record(record_entry)
        print("Contact added.")
    else:
        record.add_phone(clean_phone)
        print("Contact updated.")

@input_error
def change_contact(args: list[str], book: AddressBook) -> None:
    if len(args) < 3:
        raise IndexError

    name, old_phone,  = args[0], args[1]
    new_phone = "".join(args[2:])
    clean_new_phone = re.sub(r"[^\d+]", "", new_phone)
    record = book.find(name)

    if not record:
        raise KeyError
    if old_phone == clean_new_phone:
        raise ValueError("Phone numbers must be different.")
    record.edit_phone(old_phone, clean_new_phone)
    print("Contact updated.")

@input_error
def remove_phone(args: list[str], book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexError
    
    name = args[0]
    phone = "".join(args[1:]) 
    clean_phone = re.sub(r"[^\d+]", "", phone)
    record = book.find(name)

    if not record:
        raise KeyError
    else:
        record.remove_phone(clean_phone)
        print("Phone number removed from the record.")

@input_error
def show_phone(args: list[str], book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError

    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    print(record)

@input_error
def show_all(book: AddressBook) -> None:
    if not book:
        raise EmptyDictError
    print(book)

@input_error
def add_birthday(args, book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexError

    name, birthday, *_ = args
    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")
    elif record.birthday is None:
        record.add_birthday(birthday)
        print(f"Birthday added to {name.casefold().capitalize()}'s record.")
    else:
        raise BirthdayAlreadyExistsError(str(name))

@input_error    
def show_birthday(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError

    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    elif record.birthday is None:
        from services.exceptions import BirthdayNotSetError
        raise BirthdayNotSetError(name)
    else:
        print(f"{name.casefold().capitalize()}'s birthday is on {record.birthday}")

@input_error
def change_birthday(args, book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexError
    name, birthday, *_ = args
    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")
    record.change_birthday(birthday)    

@input_error
def birthdays(book: AddressBook):
    if not book:
        raise EmptyDictError

    from birthday import get_upcoming_birthdays
    upcoming_birthdays = get_upcoming_birthdays(book)
    heading_message = "Upcoming birthdays in your address book:"
    birthdays_list = [f"\n - {list(item.keys())[0]}: {list(item.values())[0]}" for item in upcoming_birthdays]
    final_list = [heading_message] + birthdays_list
    print("".join(final_list))


@input_error
def add_note(args, book: AddressBook) -> None:
    if len(args) < 3:
        raise IndexError

    name, title, text, *_ = args
    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")
    elif record.note is None:
        record.add_note(title, text)
        print(f"Note added to {name.casefold().capitalize()}'s record.")
    else:
        print(f"Note already exists for {name.casefold().capitalize()}. Use 'edit-note' to modify it.")
    
@input_error    
def show_note(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError

    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    elif record.note is None:
        print(f"{name.casefold().capitalize()} has no note.")
    else:
        print(f"{name.casefold().capitalize()}'s note: {record.note}")

@input_error
def remove_note(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError("Please provide name to remove.")

    name,*_ = args
    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")

    record.remove_note()
    print(f"Note  removed from {name.capitalize()}'s record.")

@input_error
def edit_note(args, book: AddressBook) -> None:
    if len(args) < 3:
        raise IndexError

    name, title, text, *_ = args
    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")
    elif record.note is None:
        print(f"{name.casefold().capitalize()} has no note to edit. Use 'add-note' to create one.")
    else:
        record.edit_note(title, text)
        print(f"Note updated for {name.casefold().capitalize()}'s record.")    

@input_error
def find_note(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError("Please provide text to search in notes.")

    query, *_ = args
    matches = book.find_by_note(query)

    if not matches:
        print(f"No notes containing '{query}' were found.")
        return

    print(f"Notes containing '{query}':")
    for record in matches:
        print(
            f"- {str(record.name).capitalize()}: "
            f"{record.note.title} — {record.note.text}"
        )
   