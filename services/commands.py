from services.exceptions import (
    EmptyDictError,
    PhoneAlreadyExistsError,
    BirthdayAlreadyExistsError,
    BirthdayNotSetError
)
from models.contact import Record
from services.address_book import AddressBook

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

    name, phone, *_ = args
    record = book.find(name)

    if not record:
        record_entry = Record(name)
        record_entry.add_phone(phone)
        book.add_record(record_entry)
        print("Contact added.")
    else:
        record.add_phone(phone)
        print("Contact updated.")

@input_error
def change_contact(args: list[str], book: AddressBook) -> None:
    if len(args) < 3:
        raise IndexError

    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    print("Contact updated.")

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
def change_birthday(args, book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexErr
