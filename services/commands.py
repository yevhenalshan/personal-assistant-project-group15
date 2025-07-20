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
from colorama import Fore
import re

# Декоратор обробки помилок
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"{Fore.RED}{e}{Fore.RESET}")
        except KeyError:
            print(f"{Fore.RED}Given username was not found in the contact list.{Fore.RESET}")
        except IndexError:
            print(f"{Fore.RED}Too few arguments were given.{Fore.RESET} Use '{Fore.GREEN}help{Fore.RESET}' for additional info.")
        except EmptyDictError:
            print(f"{Fore.RED} Address book is empty.{Fore.RESET} Add a contact with '{Fore.GREEN}add{Fore.RESET}' command.")
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
        print(f"{Fore.YELLOW}Contact added.{Fore.RESET}")
    else:
        record.add_phone(clean_phone)
        print(f"{Fore.YELLOW}Contact updated.{Fore.RESET}")

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
    print(f"{Fore.YELLOW}Contact updated.{Fore.RESET}")

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
        print(f"{Fore.YELLOW}Phone number removed from the record.{Fore.RESET}")

@input_error
def show_phone(args: list[str], book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError

    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    print(f"{Fore.GREEN}Phone records for {name.casefold().capitalize()}:{Fore.RESET} {', '.join([str(phone) for phone in record.phones])}")

def get_contacts_for_page(book: AddressBook, page, per_page):
    # Підтримка як UserDict, так і dict
    contacts = list(book.data.values()) if hasattr(book, "data") else list(book.values())
    total_pages = (len(contacts) + per_page - 1) // per_page
    start = page * per_page
    end = start + per_page
    return contacts[start:end], total_pages

# Глобальні змінні для пагінації
current_page = 0
contacts_per_page = 5

@input_error
def show_all_with_pagination(book: AddressBook):
    global current_page, contacts_per_page
    contacts, total_pages = get_contacts_for_page(book, current_page, contacts_per_page)
    if not contacts:
        raise EmptyDictError
    print(f"{Fore.GREEN}Your contact list (page {current_page + 1} of {total_pages}):{Fore.RESET}")
    for record in contacts:
        print("-" * 30)
        print(record)
    print("-" * 30)
    if total_pages > 1:
        if current_page == 0:
            print(f"You're on the first page. Type {Fore.GREEN}'next'{Fore.RESET} to go forward.")
        elif current_page == total_pages - 1:
            print(f"You're on the last page. Type {Fore.GREEN}'prev'{Fore.RESET} to go back.")
        else:
            print(f"Type {Fore.GREEN}'next'{Fore.RESET} or {Fore.GREEN}'prev'{Fore.RESET} to switch pages.")

def next_page(book: AddressBook):
    global current_page, contacts_per_page
    _, total_pages = get_contacts_for_page(book, current_page, contacts_per_page)
    if current_page < total_pages - 1:
        current_page += 1
        show_all_with_pagination(book)
    else:
        print(f"{Fore.BLUE}You're already on the last page.{Fore.RESET}")

def prev_page(book: AddressBook):
    global current_page
    if current_page > 0:
        current_page -= 1
        show_all_with_pagination(book)
    else:
        print(f"{Fore.BLUE}You're already on the first page.{Fore.RESET}")


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
        print(f"{Fore.YELLOW}Birthday added to {name.casefold().capitalize()}'s record.{Fore.RESET}")
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
        print(f"{Fore.YELLOW}Birthday date updated.{Fore.RESET}")

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
        print(f"{Fore.YELLOW}{name.casefold().capitalize()}'s birthday is on {record.birthday}{Fore.RESET}")

@input_error
def birthdays(args: list[str], book: AddressBook) -> None:
    if not book:
        raise EmptyDictError

    upcoming_birthdays = get_upcoming_birthdays(book) if len(args) < 1 else get_upcoming_birthdays(book, days=int(args[0]))
    heading_message = f"{Fore.GREEN}Upcoming birthdays in your address book:{Fore.RESET}"
    birthdays_list = [f"\n - {list(item.keys())[0]}: {list(item.values())[0]}" for item in upcoming_birthdays]
    if not birthdays_list:
        raise ValueError("There are no upcoming birthday for given number of days.")
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
        print(f"{Fore.YELLOW}Email added to {name.casefold().capitalize()}'s record.{Fore.RESET}")

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
    print(f"{Fore.YELLOW}Email updated.{Fore.RESET}")

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
        start_string = f"{Fore.GREEN}{name.casefold().capitalize()}'s emails are:{Fore.RESET}"
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
        print(f"{Fore.YELLOW}Email {email} was removed from {name.casefold().capitalize()}'s record.{Fore.RESET}")

@input_error
def emails(book: AddressBook):
    result = f"{Fore.GREEN}Email addresses available:{Fore.RESET}"
    for name, record in book.items():
        result += (f"\n- {name}: " +  ", ".join([email.value for email in record.emails if record.emails]))
    print(result)

@input_error
def add_note(args, book: AddressBook) -> None:
    if len(args) < 3:
        raise ValueError("Usage: add_note <name> <title> <text> [tags...]")

    name = args[0]
    title = args[1]
    
    # Everything after title is text, until tags are found
    text_parts = []
    tags = []
    for arg in args[2:]:
        # Check if this looks like a tag (in brackets or single quoted string with commas)
        if (arg.startswith('[') and arg.endswith(']')) or \
           (arg.startswith('"') and arg.endswith('"') and ',' in arg and arg.count('"') == 2):
            tags.append(arg)
            break
        else:
            text_parts.append(arg)
    text = " ".join(text_parts)

    # Parse tags if they're provided in bracket notation like ["tag1,tag2"] or quoted string
    if tags:
        tag_str = tags[0]
        if tag_str.startswith('[') and tag_str.endswith(']'):
            tag_str = tag_str[1:-1]  # Remove brackets
        if tag_str.startswith('"') and tag_str.endswith('"'):
            tag_str = tag_str[1:-1]  # Remove quotes
        tags = [tag.strip().replace('"', '') for tag in tag_str.split(',')]

    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")

    if record.note is None:
        record.add_note(title, text, tags)
        print(f"{Fore.YELLOW}Note added to {name.casefold().capitalize()}'s record.{Fore.RESET}")
    else:
        print(f"{Fore.RED}Note already exists for {name.casefold().capitalize()}.{Fore.RESET} Use {Fore.GREEN}'edit-note'{Fore.RESET} to modify it.")
    
@input_error    
def show_note(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    elif record.note is None:
        raise ValueError(f"{name.casefold().capitalize()} has no note.")
    else:
        print(f"{Fore.GREEN}{name.casefold().capitalize()}'s note:{Fore.RESET} {record.note}")

@input_error
def remove_note(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError

    name,*_ = args
    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")

    record.remove_note()
    print(f"{Fore.YELLOW}Note  removed from {name.capitalize()}'s record.{Fore.RESET}")

@input_error
def edit_note(args, book: AddressBook) -> None:
    if len(args) < 3:
        raise ValueError("Usage: edit-note <name> <title> <text> [tags...]")

    name = args[0]
    title = args[1]
    
    # Everything after title is text, until tags are found
    text_parts = []
    tags = []
    for arg in args[2:]:
        # Check if this looks like a tag (in brackets or single quoted string with commas)
        if (arg.startswith('[') and arg.endswith(']')) or \
           (arg.startswith('"') and arg.endswith('"') and ',' in arg and arg.count('"') == 2):
            tags.append(arg)
            break
        else:
            text_parts.append(arg)
    text = " ".join(text_parts)

    # Parse tags if they're provided in bracket notation like ["tag1,tag2"] or quoted string
    if tags:
        tag_str = tags[0]
        if tag_str.startswith('[') and tag_str.endswith(']'):
            tag_str = tag_str[1:-1]  # Remove brackets
        if tag_str.startswith('"') and tag_str.endswith('"'):
            tag_str = tag_str[1:-1]  # Remove quotes
        tags = [tag.strip().replace('"', '') for tag in tag_str.split(',')]

    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")
    elif record.note is None:
        print(f"{Fore.RED}{name.casefold().capitalize()} has no note to edit.{Fore.RESET} Use {Fore.GREEN}'add-note'{Fore.RESET} to create one.")
    else:
        record.edit_note(title, text, tags)
        print(f"{Fore.YELLOW}Note updated for {name.casefold().capitalize()}'s record.{Fore.RESET}")

@input_error
def find_note(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError

    query, *_ = args
    matches = book.find_by_note(query)

    if not matches:
        raise ValueError(f"No notes containing '{query}' were found.")

    print(f"{Fore.GREEN}Notes containing '{query}':{Fore.RESET}")
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
        print(f"{Fore.RED}Residential address is already set for {name.casefold().capitalize()}.{Fore.RESET} Use {Fore.GREEN}'change-address'{Fore.RESET} to change it.")
    else:
        record.add_address(address)
        print(f"{Fore.YELLOW}Residential address added to {name.casefold().capitalize()}'s record.{Fore.RESET}")

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
        print(f"{Fore.YELLOW}Residential address updated.{Fore.RESET}")

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
        print(f"{name.casefold().capitalize()}'s residential address is {record.address}")

@input_error
def delete_record(args: list[str], book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError
    
    name, *_ = args
    deleted = book.delete(name)
    if deleted is None:
        raise KeyError
    else:
        print(f"{Fore.YELLOW}{name.casefold().capitalize()}'s record deleted.{Fore.RESET}")


@input_error
def find_by_tags(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError

    tags = args
    matches = book.find_by_tags(tags)

    if not matches:
        raise ValueError(f"No notes with tags {tags} were found.")

    print(f"Notes with tags {tags}:")
    for record, matching_tags in matches:
        # Handle both list format and comma-separated string format for display
        note_tags = record.note.tags
        if isinstance(note_tags, list):
            # Check if it's a list of individual tags or a list with one comma-separated string
            if len(note_tags) == 1 and ',' in note_tags[0]:
                # Handle case like ["tag1,tag2"] - list with one comma-separated string
                tags_str = f" [Tags: {note_tags[0]}]"
            else:
                # Handle case like ["tag1", "tag2"] - list of individual tags
                tags_str = f" [Tags: {', '.join(note_tags)}]" if note_tags else ""
        else:
            # If tags are stored as a comma-separated string, format them properly
            note_tags_str = str(note_tags)
            # Handle the case where the entire string is quoted like "tag1,tag2"
            if note_tags_str.startswith('"') and note_tags_str.endswith('"'):
                note_tags_str = note_tags_str[1:-1]  # Remove outer quotes
            # Also handle the case where it's in list format like ["tag1,tag2"]
            if note_tags_str.startswith('[') and note_tags_str.endswith(']'):
                note_tags_str = note_tags_str[1:-1]  # Remove brackets
            tags_str = f" [Tags: {note_tags_str}]" if note_tags_str else ""
        
        print(
            f"- {str(record.name).capitalize()}: "
            f"{record.note.title} — {record.note.text}{tags_str}"
        )
        print(f"{Fore.GREEN}  Matching tags:{Fore.RESET} {', '.join(matching_tags)}")

@input_error
def search_contact(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError

    query, *_ = args
    matches = book.search_by_name(query)

    if not matches:
        raise ValueError(f"No contacts found containing '{query}' in their name.")

    print(f"{Fore.GREEN}Contacts found containing '{query}':{Fore.RESET}")
    for record in matches:
        print(f"- {str(record.name).capitalize()}: {record}")
