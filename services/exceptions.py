class ArgumentInstanceError(Exception):
    pass

class EmptyDictError(Exception):
    pass

class PhoneAlreadyExistsError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"Given phone number is already in {str(self.name)}'s record."

class BirthdayAlreadyExistsError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.casefold().capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"{self.name}'s birthday is already set. Use 'change-birthday' to edit the date."

class BirthdayNotSetError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.casefold().capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"{str(self.name)} does not have a birthday date set. Use 'add-birthday' to add the date."

class EmailAlreadyExistsError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"Given email is already in {str(self.name)}'s record."
    
class EmailNotSetError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.casefold().capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"{str(self.name)} does not have any email addresses set. Use 'add-email' to add the address."
    
class AddressNotSetError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name.casefold().capitalize()
        super().__init__(name)

    def __str__(self) -> str:
        return f"{str(self.name)} does not have a residential address set. Use 'add-address' to add the address."