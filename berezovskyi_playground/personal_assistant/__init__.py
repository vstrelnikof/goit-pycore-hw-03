"""
Персональний помічник - консольна програма для управління контактами та нотатками

Основні компоненти:
- address_book: Модуль для роботи з контактами
- notes: Модуль для роботи з нотатками  
- utils: Допоміжні утиліти (парсер команд)
"""
from .address_book import AddressBook, Record
from .notes import NoteBook, Note
from .utils import CommandParser

__version__ = '2.0'
__all__ = [
    'AddressBook',
    'Record',
    'NoteBook',
    'Note',
    'CommandParser'
]
