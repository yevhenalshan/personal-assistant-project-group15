from storage import load_data, save_data
from services.address_book import AddressBook
from services.commands import (
    add_contact, change_contact, show_phone, show_all, remove_phone,
    add_birthday, change_birthday, show_birthday, birthdays
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
    * all - get all contacts from the contact list
    * exit - close the program
    * close - close the program"""
                )
            else:
                print("Unknown command was given. Use 'help' for additional info.")
    except KeyboardInterrupt:
        save_data(book)
