from storage import load_data, save_data
from services.address_book import AddressBook
from services.commands import (
    add_contact, change_contact, show_phone, show_all, remove_phone,
    add_birthday, change_birthday, show_birthday, birthdays, add_email,
    change_email, show_email, remove_email, emails
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

            match command:
                case "hello":
                    print("How can I help you?")
                case "add":
                    add_contact(args, book)
                case "change":
                    change_contact(args, book)
                case "phone":
                    show_phone(args, book)
                case "remove":
                    remove_phone(args, book)
                case "all":
                    show_all(book)
                case "add-birthday":
                    add_birthday(args, book)
                case "change-birthday":
                    change_birthday(args, book)
                case "show-birthday":
                    show_birthday(args, book)
                case "birthdays":
                    birthdays(book)
                case "add-email":
                    add_email(args, book)
                case "change-email":
                    change_email(args, book)
                case "show-email":
                    show_email(args, book)
                case "emails":
                    emails(book)
                case "remove-email":
                    remove_email(args, book)
                case "close" | "exit":
                    save_data(book)
                    print("Goodbye!")
                    break
                case "help":
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
    * add-email [username] [email] - add an email address to a contact record
    * change-email [username] [old_email] [new_email] - change given email address of a contact
    * remove-email [username] [email] - remove an already existing email address from a contact record
    * show-email [username] - get to know an email address for a given contact
    * emails - get to know all the emails saved in your contact book
    * all - get all contacts from the contact list
    * exit - close the program
    * close - close the program"""
                    )
                case _:
                    print("Unknown command was given. Use 'help' for additional info.")
    except KeyboardInterrupt:
        save_data(book)
