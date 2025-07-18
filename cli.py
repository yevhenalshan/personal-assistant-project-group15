from storage import load_data, save_data
from services.address_book import AddressBook

from services.commands import (
    add_contact,  add_note, edit_note, find_note, find_by_tags, remove_note, show_note,
    change_contact, show_phone, show_all, remove_phone, add_birthday,
    change_birthday, show_birthday, birthdays, add_email, change_email,
    show_email, remove_email, emails, add_address, change_address,
    show_address, delete_record
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
                    birthdays(args, book)
                case "add-email":
                    add_email(args, book)
                case "change-email":
                    change_email(args, book)
                case "show-email":
                    show_email(args, book)
                case "remove-email":
                    remove_email(args, book)
                case "emails":
                    emails(book)
                case "add-address":
                    add_address(args, book)
                case "change-address":
                    change_address(args, book)
                case "show-address":
                    show_address(args, book)
                case "delete":
                    delete_record(args, book)
                case "add-note":
                    add_note(args, book)
                case "show-note":
                    show_note(args, book)     
                case "remove-note":
                    remove_note(args, book)    
                case "edit-note":
                    edit_note(args, book)
                case "find-note":
                    find_note(args, book)
                case "find-by-tags":
                    find_by_tags(args, book)
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
    * add-note [username] [title] [text] [tags...] - add a note to a contact (tags can be individual words or ["tag1,tag2"] format)
    * show-note [username] - show a contact's note
    * edit-note [username] [title] [text] [tags...] - edit a contact's note (tags are optional)
    * remove-note [username] - remove a contact's note
    * find-note [query] - search for notes containing the query text
    * add-address [name] [address] - add a residential address to a contact record 
    * change-address [name] [new_address] - change the residential address for a contact record 
    * show-address [name] - get to know the residential address of a contact
    * find-by-tags [tag1] [tag2] ... - search for notes with specific tags
    * search [name] - search for contacts by name (partial match)
    * delete [name] - delete a record
    * all - get all contacts from the contact list
    * exit - close the program
    * close - close the program"""
                    )
                case _:
                    print("Unknown command was given. Use 'help' for additional info.")
    except KeyboardInterrupt:
        save_data(book)
