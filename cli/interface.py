from managers.address_book import AddressBook
from managers.notes_manager import NotesManager

class CLI:
    def __init__(self):
        self.address_book = AddressBook()
        self.notes_manager = NotesManager()

    def run(self):
        print("=== Персональний помічник ===")
        print("Команди: add_contact, list_contacts, search_contact, edit_contact, delete_contact, birthdays, add_note, list_notes, search_note, edit_note, delete_note, exit")

        while True:
            command = input("\nВведіть команду: ").strip().lower()

            match command:
                case "add_contact": self.address_book.add_contact()
                case "list_contacts": self.address_book.list_contacts()
                case "search_contact": self.address_book.search_contact()
                case "edit_contact": self.address_book.edit_contact()
                case "delete_contact": self.address_book.delete_contact()
                case "birthdays": self.address_book.upcoming_birthdays()
                case "add_note": self.notes_manager.add_note()
                case "list_notes": self.notes_manager.list_notes()
                case "search_note": self.notes_manager.search_note()
                case "edit_note": self.notes_manager.edit_note()
                case "delete_note": self.notes_manager.delete_note()
                case "exit": exit()
                case _: print("❌ Невідома команда")