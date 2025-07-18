from services.exceptions import (
    EmptyDictError,
    PhoneAlreadyExistsError,
    BirthdayAlreadyExistsError,
    BirthdayNotSetError,
    EmailAlreadyExistsError,
    EmailNotSetError,
    AddressNotSetError
)
from models.contact import Record
from services.address_book import AddressBook
from birthday import get_upcoming_birthdays
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
        except (PhoneAlreadyExistsError, BirthdayAlreadyExistsError, BirthdayNotSetError, EmailAlreadyExistsError, EmailNotSetError, AddressNotSetError) as e:
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
    record.change_phone(old_phone, clean_new_phone)
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
def add_birthday(args: list[str], book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexError

    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    elif record.birthday is None:
        record.add_birthday(birthday)
        print(f"Birthday added to {name.casefold().capitalize()}'s record.")
    else:
        raise BirthdayAlreadyExistsError(str(name))

@input_error
def change_birthday(args: list[str], book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexError
    
    name, birthday, *_ = args
    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")
    elif birthday == record.birthday.value:
        raise ValueError("New birthday date must differ from the old one.")
    else:
        record.change_birthday(birthday)
        print("Birthday date updated.")

@input_error    
def show_birthday(args: list[str], book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError

    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    elif record.birthday is None:
        raise BirthdayNotSetError(name)
    else:
        print(f"{name.casefold().capitalize()}'s birthday is on {record.birthday}")

@input_error
def birthdays(args: list[str], book: AddressBook) -> None:
    if not book:
        raise EmptyDictError

    upcoming_birthdays = get_upcoming_birthdays(book) if len(args) < 1 else get_upcoming_birthdays(book, days=int(args[0]))
    heading_message = "Upcoming birthdays in your address book:"
    birthdays_list = [f"\n - {list(item.keys())[0]}: {list(item.values())[0]}" for item in upcoming_birthdays]
    if not birthdays_list:
        print("There are no upcoming birthday for next week.") #TODO: підставити задану користувачем кількість днів
    final_list = [heading_message] + birthdays_list
    print("".join(final_list))

@input_error
def add_email(args: list[str], book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexError
    
    name, email, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError 
    else:
        record.add_email(email)
        print(f"Email added to {name.casefold().capitalize()}'s record.")

@input_error
def change_email(args: list[str], book: AddressBook) -> None:
    if len(args) < 3:
        raise IndexError
    
    name, old_email, new_email, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if old_email == new_email:
        raise ValueError("Emails must be different.")
    record.change_email(old_email, new_email)
    print("Email updated.")

@input_error
def show_email(args: list[str], book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    elif not record.emails:
        raise EmailNotSetError(name)
    else:
        start_string = f"{name.casefold().capitalize()}'s emails are:"
        emails_data = [f"\n- {email}" for email in record.emails]
        result_string = start_string + "".join(emails_data)
        print(result_string)
    
@input_error
def remove_email(args: list[str], book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexError

    name, email, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    elif not record.emails:
        raise EmailNotSetError(name)
    else:
        record.remove_email(email)
        print(f"Email {email} was removed from {name.casefold().capitalize()}'s record.")

@input_error
def emails(book: AddressBook):
    result = "Email addresses available:"
    for name, record in book.items():
        result += (f"\n- {name}: " +  ", ".join([email.value for email in record.emails if record.emails]))
    print(result)

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


@input_error
def add_address(args: list[str], book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexError
    
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)

    if record is None:
        raise KeyError
    elif record.address:
        raise ValueError(f"Residential address is already set for {name.casefold().capitalize()}. Use 'change-address' to change it.")
    else:
        record.add_address(address)
        print(f"Residential address added to {name.casefold().capitalize()}'s record.")

@input_error
def change_address(args: list[str], book: AddressBook) -> None:
    if len(args) < 2:
        raise IndexError
    
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)

    if record is None:
        raise KeyError
    else:
        record.change_address(address)
        print("Residential address updated.")

@input_error
def show_address(args: list[str], book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError
    
    name, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError
    elif record.address is None:
        raise AddressNotSetError(name)
    else:
        # print(str(record.address))
        print(f"{name.casefold().capitalize()}'s residential address is {record.address}")

@input_error
def delete_record(args: list[str], book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError
    
    name, *_ = args
    book.delete(name)