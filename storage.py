import pickle
from services.address_book import AddressBook

def load_data(filename="user_data/addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def save_data(book, filename="user_data/addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)
