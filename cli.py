from storage import load_data, save_data
from services.commands import (
    add_contact, add_note, edit_note, find_note, find_by_tags, remove_note, show_note,
    change_contact, show_phone, remove_phone, add_birthday,
    change_birthday, show_birthday, birthdays, add_email, change_email,
    show_email, remove_email, emails, add_address, change_address,
    show_address, search_contact, delete_record, show_all_with_pagination, 
    next_page, prev_page
)
from parser import parse_input
from colorama import Fore

HELP_MESSAGE = f"""The following commands are available:
    * {Fore.GREEN + 'add <username> <phone_number>':<60}{Fore.RESET} - add a contact to the contact list. note: phone number must consist of 10 digits
    * {Fore.GREEN + 'change <username> <old_phone_number> <new_phone_number>':<60}{Fore.RESET} - change an already existing contact
    * {Fore.GREEN + 'phone <username>':<60}{Fore.RESET} - get to know a phone number by the contact's username
    * {Fore.GREEN + 'remove <username> <phone_number>':<60}{Fore.RESET} - remove phone number from a person's record
    * {Fore.GREEN + 'add-birthday <username> <birthday>':<60}{Fore.RESET} - set a birthday date for a contact
    * {Fore.GREEN + 'change-birthday <username> <new_birthday>':<60}{Fore.RESET} - change birthday date for a contact
    * {Fore.GREEN + 'show-birthday <username>':<60}{Fore.RESET} - get to know the birthday date of the contact
    * {Fore.GREEN + 'birthdays *days*':<60}{Fore.RESET} - get to know birthdays from your address book for a given number of days (week by default)
    * {Fore.GREEN + 'add-email <username> <email>':<60}{Fore.RESET} - add an email address to a contact record
    * {Fore.GREEN + 'change-email <username> <old_email> <new_email>':<60}{Fore.RESET} - change given email address of a contact
    * {Fore.GREEN + 'remove-email <username> <email>':<60}{Fore.RESET} - remove an already existing email address from a contact record
    * {Fore.GREEN + 'show-email <username>':<60}{Fore.RESET} - get to know an email address for a given contact
    * {Fore.GREEN + 'emails':<60}{Fore.RESET} - get to know all the emails saved in your contact book   
    * {Fore.GREEN + 'add-note <username> <title> <text> [tags...]':<60}{Fore.RESET} - add a note to a contact (tags can be individual words or ["tag1", "tag2"] format)
    * {Fore.GREEN + 'show-note <username>':<60}{Fore.RESET} - show a contact's note
    * {Fore.GREEN + 'edit-note <username> <title> <text> [tags...]':<60}{Fore.RESET} - edit a contact's note (tags are optional)
    * {Fore.GREEN + 'remove-note <username>':<60}{Fore.RESET} - remove a contact's note
    * {Fore.GREEN + 'find-note <query>':<60}{Fore.RESET} - search for notes containing the query text
    * {Fore.GREEN + 'add-address <name> <address>':<60}{Fore.RESET} - add a residential address to a contact record 
    * {Fore.GREEN + 'change-address <name> <new_address>':<60}{Fore.RESET} - change the residential address for a contact record 
    * {Fore.GREEN + 'show-address <name>':<60}{Fore.RESET} - get to know the residential address of a contact
    * {Fore.GREEN + 'find-by-tags <tag1> <tag2> ...':<60}{Fore.RESET} - search for notes with specific tags
    * {Fore.GREEN + 'search <name>':<60}{Fore.RESET} - search for contacts by name (partial match)
    * {Fore.GREEN + 'delete <name>':<60}{Fore.RESET} - delete a record
    * {Fore.GREEN + 'all':<60}{Fore.RESET} - get all contacts from the contact list (5 per page; use 'next'/'prev' for pagination)
    * {Fore.GREEN + 'exit':<60}{Fore.RESET} - close the program
    * {Fore.GREEN + 'close':<60}{Fore.RESET} - close the program"""

COMMANDS = {
    "hello": lambda args, book: print(f"{Fore.YELLOW}How can I help you?{Fore.RESET}"),
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "remove": remove_phone,
    "add-birthday": add_birthday,
    "change-birthday": change_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "add-email": add_email,
    "change-email": change_email,
    "show-email": show_email,
    "remove-email": remove_email,
    "emails": lambda args, book: emails(book),
    "add-note": add_note,
    "show-note": show_note,
    "edit-note": edit_note,
    "remove-note": remove_note,
    "find-note": remove_note,
    "find-note": find_note,
    "find-by-tags": find_by_tags,
    "add-address": add_address,
    "change-address": change_address,
    "show-address": show_address,
    "delete": delete_record,
    "search": search_contact,
    "all": lambda args, book: show_all_with_pagination(book),
    "next": lambda args, book: next_page(book),
    "prev": lambda args, book: prev_page(book),
    "help": lambda args, book: print(HELP_MESSAGE)
}


COMMANDS["?"] = COMMANDS["help"]
COMMANDS["commands"] = COMMANDS["help"]

EXIT_COMMANDS = {"exit", "close"}

def run_cli():
    book = load_data()
    print("Welcome to the assistant bot!")
    try:
        while True:

            user_input = input("Enter a command: ").strip().casefold()
            if len(user_input) < 1:
                print(f"{Fore.RED}Too few arguments were given.{Fore.RESET} Use {Fore.GREEN}'help'{Fore.RESET} for additional info.")
                continue

            command, args = parse_input(user_input)

            if command in EXIT_COMMANDS:
                save_data(book)
                print(f"{Fore.YELLOW}Goodbye!{Fore.RESET}")
                break
            
            handler = COMMANDS.get(command)

            if handler:
                handler(args, book)
            else:
                print(f"{Fore.RED}Unknown command was given.{Fore.RESET} Use {Fore.GREEN}'help'{Fore.RESET} for additional info.")
    except KeyboardInterrupt:
        save_data(book)
