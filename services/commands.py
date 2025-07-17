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
        raise IndexError("Usage: add_note <name> <title> <text> [tags...]")

    name = args[0]
    title = args[1]
    text = args[2]
    tags = args[3:]  # всё, что идёт после текста — это теги
    
    # Parse tags if they're provided in bracket notation like ["tag1,tag2"]
    if tags and len(tags) == 1 and tags[0].startswith('[') and tags[0].endswith(']'):
        # Handle bracket notation like ["tag1,tag2"]
        tag_str = tags[0][1:-1]  # Remove brackets
        if tag_str.startswith('"') and tag_str.endswith('"'):
            tag_str = tag_str[1:-1]  # Remove quotes
        tags = [tag.strip() for tag in tag_str.split(',')]

    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")

    if record.note is None:
        record.add_note(title, text, tags)
        print(f"Note added to {name.capitalize()}'s record.")
    else:
        print(f"Note already exists for {name.capitalize()}. Use 'edit-note' to modify it.")
    
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
        raise IndexError("Usage: edit-note <name> <title> <text> [tags...]")

    name = args[0]
    title = args[1]
    text = args[2]
    tags = args[3:] if len(args) > 3 else None  # Tags are optional
    
    # Parse tags if they're provided in bracket notation like ["tag1,tag2"]
    if tags and len(tags) == 1 and tags[0].startswith('[') and tags[0].endswith(']'):
        # Handle bracket notation like ["tag1,tag2"]
        tag_str = tags[0][1:-1]  # Remove brackets
        if tag_str.startswith('"') and tag_str.endswith('"'):
            tag_str = tag_str[1:-1]  # Remove quotes
        tags = [tag.strip() for tag in tag_str.split(',')]

    record = book.find(name)
    if not record:
        raise ValueError(f"Record with name '{name}' was not found.")
    elif record.note is None:
        print(f"{name.casefold().capitalize()} has no note to edit. Use 'add-note' to create one.")
    else:
        record.edit_note(title, text, tags)
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
def find_by_tags(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError("Please provide at least one tag to search for.")

    tags = args
    matches = book.find_by_tags(tags)

    if not matches:
        print(f"No notes with tags {tags} were found.")
        return

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
        print(f"  Matching tags: {', '.join(matching_tags)}")

@input_error
def search_contact(args, book: AddressBook) -> None:
    if len(args) < 1:
        raise IndexError("Please provide a name to search for.")

    query, *_ = args
    matches = book.search_by_name(query)

    if not matches:
        print(f"No contacts found containing '{query}' in their name.")
        return

    print(f"Contacts found containing '{query}':")
    for record in matches:
        print(f"- {str(record.name).capitalize()}: {record}")
   