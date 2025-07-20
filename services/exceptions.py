from colorama import Fore

class ArgumentInstanceError(Exception):
    pass

class EmptyDictError(Exception):
    pass

class PhoneAlreadyExistsError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"{Fore.RED}Given phone number is already in {str(self.name)}'s record.{Fore.RESET}"

class BirthdayAlreadyExistsError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.casefold().capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"{Fore.RED}{self.name}'s birthday is already set.{Fore.RESET} Use {Fore.GREEN}'change-birthday'{Fore.RESET} to edit the date."

class BirthdayNotSetError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.casefold().capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"{Fore.RED}{self.name} does not have a birthday date set.{Fore.RESET} Use {Fore.GREEN}'add-birthday'{Fore.RESET} to add the date."

class EmailAlreadyExistsError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"{Fore.RED}Given email is already in {str(self.name)}'s record.{Fore.RESET}"
    
class EmailNotSetError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.casefold().capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"{Fore.RED}{self.name} does not have any email addresses set.{Fore.RESET} Use {Fore.GREEN}'add-email'{Fore.RESET} to add the address."
    
class AddressNotSetError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.casefold().capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"{Fore.RED}{self.name} does not have a residential address set.{Fore.RESET} Use {Fore.GREEN}'add-address'{Fore.RESET} to add the address."