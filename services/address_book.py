from collections import UserDict
from services.exceptions import ArgumentInstanceError
from models.contact import Record

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        if not isinstance(record, Record):
            raise ArgumentInstanceError("The argument must be a record")
        elif str(record.name) in self.data.keys():
            raise ValueError("Name is already in address book")
        self.data[str(record.name)] = record

    def find(self, name: str):
        try:
            return self.data[name.casefold()]
        except KeyError:
            return None

    def delete(self, name: str) -> None:
        try:
            self.data.pop(name.casefold())
        except KeyError:
            return None

    def __str__(self) -> str:
        result = ""
        for name, record in self.data.items():
            result += str(record) + "\n"
        return result.strip()
