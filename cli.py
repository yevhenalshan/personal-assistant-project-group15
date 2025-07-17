from storage import load_data, save_data
from services.address_book import AddressBook
from services.commands import (add_contact, add_note, change_contact, edit_note, find_note, find_by_tags, remove_note, show_note, show_phone, show_all, remove_phone,
     add_birthday, change_birthday, show_birthday, birthdays, search_contact
)
from parser import parse_input

def run_cli():
    book = load_data()
    print("Welcome to the assistant bot!")
    try:
        while True:
            user_input = input("Enter a command: ").strip().casefold()
            if len(user_input) < 1:
                print("Too few arguments were given. Use 'help' for additional info.")
                continue

            command, args = parse_input(user_input)

            if command == "hello":
                print("How can I help you?")
            elif command == "add":
                add_contact(args, book)
            elif command == "change":
                change_contact(args, book)
            elif command == "phone":
                show_phone(args, book)
            elif command == "remove":
                remove_phone(args, book)
            elif command == "all":
                show_all(book)
            elif command == "add-birthday":
                add_birthday(args, book)
            elif command == "change-birthday":
                change_birthday(args, book)
            elif command == "show-birthday":
                show_birthday(args, book)   
            elif command == "birthdays":
                birthdays(book)
            elif command == "add-note":
                add_note(args, book)    
            elif command == "show-notes":
                show_note(args, book)     
            elif command == "remove-note":
                remove_note(args, book)    
            elif command == "edit-note":
                edit_note(args, book)
            elif command == "find-note":
                find_note(args, book)
            elif command == "find-by-tags":
                find_by_tags(args, book)
            elif command == "search":
                search_contact(args, book)            
            elif command in ("close", "exit"):
                save_data(book)
                print("Goodbye!")
                break
            elif command == "help":
                print(
"""The following commands are available:
    * add [username] [phone_number] - add a contact to the contact list. note: phone number must consist of 10 digits
    * change [username] [old_phone_number] [new_phone_number] - change an already existing contact
    * phone [username] - get to know a phone number by the contact's username
    * remove [username] [phone_number] - remove phone number from a person's record
    * add-birthday [username] [birthday] - set a birthday date for a contact
    * change-birthday [username] [new_birthday] - change birthday date for a contact
    * show-birthday [username] - get to know the birthday date of the contact
    * birthdays - get to know birthdays from your address book for upcoming week
    * add-note [username] [title] [text] [tags...] - add a note to a contact (tags can be individual words or ["tag1,tag2"] format)
    * show-notes [username] - show a contact's note
    * edit-note [username] [title] [text] [tags...] - edit a contact's note (tags are optional)
    * remove-note [username] - remove a contact's note
    * find-note [query] - search for notes containing the query text
    * find-by-tags [tag1] [tag2] ... - search for notes with specific tags
    * search [name] - search for contacts by name (partial match)
    * all - get all contacts from the contact list
    * exit - close the program
    * close - close the program"""
                )
            else:
                print("Unknown command was given. Use 'help' for additional info.")
    except KeyboardInterrupt:
        save_data(book)
