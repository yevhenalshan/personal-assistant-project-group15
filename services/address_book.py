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

    def find(self, name: str) -> Record | None:
        try:
            return self.data[name.casefold()]
        except KeyError:
            return None

    def search_by_name(self, query: str) -> list[Record]:
        """
        Returns a list of Records where the name contains the query string (case-insensitive).
        """
        results = []
        query_lower = query.casefold()
        
        for record in self.data.values():
            if query_lower in str(record.name).casefold():
                results.append(record)
        
        return results

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

    def find_by_tags(self, tags: list[str]):
        """
        Returns a list of Records where the note contains any of the specified tags (case-insensitive).
        """
        results = []
        for record in self.data.values():
            try:
                if record.note and hasattr(record.note, 'tags') and record.note.tags:
                    # Handle both list format and comma-separated string format
                    note_tags = record.note.tags
                    if isinstance(note_tags, list):
                        # If tags are already in list format
                        # Check if it's a list of individual tags or a list with one comma-separated string
                        if len(note_tags) == 1 and ',' in note_tags[0]:
                            # Handle case like ["tag1,tag2"] - list with one comma-separated string
                            note_tags_str = note_tags[0]
                            note_tags_lower = [tag.strip().casefold() for tag in note_tags_str.split(',')]
                        else:
                            # Handle case like ["tag1", "tag2"] - list of individual tags
                            note_tags_lower = [tag.casefold() for tag in note_tags]
                    else:
                        # If tags are stored as a comma-separated string, split them
                        note_tags_str = str(note_tags)
                        # Handle the case where the entire string is quoted like "tag1,tag2"
                        if note_tags_str.startswith('"') and note_tags_str.endswith('"'):
                            note_tags_str = note_tags_str[1:-1]  # Remove outer quotes
                        # Also handle the case where it's in list format like ["tag1,tag2"]
                        if note_tags_str.startswith('[') and note_tags_str.endswith(']'):
                            note_tags_str = note_tags_str[1:-1]  # Remove brackets
                        note_tags_lower = [tag.strip().casefold() for tag in note_tags_str.split(',')]
                    
                    search_tags_lower = [tag.casefold() for tag in tags]
                    
                    # Find matching tags
                    matching_tags = [tag for tag in search_tags_lower if tag in note_tags_lower]
                    
                    if matching_tags:
                        results.append((record, matching_tags))
            except AttributeError:
                # Skip records that don't have proper note structure
                continue
        return results     

    def __str__(self) -> str:
        result = ""
        for name, record in self.data.items():
            result += str(record) + "\n"
        return result.strip()
