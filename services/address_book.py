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
        
    def find_by_note(self, query: str):
        """
        Returns a list of Records where the note title or text contains the query string (case-insensitive).
        """
        results = []
        for record in self.data.values():
            try:
                if record.note and hasattr(record.note, 'title') and hasattr(record.note, 'text'):
                    title_match = query.casefold() in record.note.title.casefold()
                    text_match = query.casefold() in record.note.text.casefold()
                    if title_match or text_match:
                        results.append(record)
            except AttributeError:
                # Skip records that don't have proper note structure
                continue
        return results     

    def __str__(self) -> str:
        result = ""
        for name, record in self.data.items():
            result += str(record) + "\n"
        return result.strip()
