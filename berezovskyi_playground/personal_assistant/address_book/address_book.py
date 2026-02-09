"""
Клас AddressBook для управління контактами
"""
from collections import UserDict
import json
from pathlib import Path
from .models import Record


class AddressBook(UserDict):
    """Клас для зберігання та управління записами"""
    def __init__(self, data_dir=None):
        super().__init__()
        if data_dir is None:
            # За замовчуванням зберігаємо в папці проекту
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data"
        else:
            data_dir = Path(data_dir)
        
        data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = data_dir / "contacts.json"

    def add_record(self, record):
        """Додавання запису"""
        self.data[record.name.value] = record

    def find(self, name):
        """Пошук запису за ім'ям"""
        return self.data.get(name)

    def delete(self, name):
        """Видалення запису"""
        if name in self.data:
            del self.data[name]

    def search(self, query):
        """Пошук контактів за різними критеріями"""
        results = []
        query_lower = query.lower()
        
        for record in self.data.values():
            # Пошук за ім'ям
            if query_lower in record.name.value.lower():
                results.append(record)
                continue
            
            # Пошук за телефоном
            if any(query in phone.value for phone in record.phones):
                results.append(record)
                continue
            
            # Пошук за email
            if record.email and query_lower in record.email.value.lower():
                results.append(record)
                continue
            
            # Пошук за адресою
            if record.address and query_lower in record.address.value.lower():
                results.append(record)
                continue
        
        return results

    def get_birthdays_in_days(self, days):
        """Отримання списку контактів з днем народження через задану кількість днів"""
        results = []
        for record in self.data.values():
            days_to_bd = record.days_to_birthday()
            if days_to_bd is not None and days_to_bd <= days:
                results.append((record, days_to_bd))
        
        # Сортування за кількістю днів
        results.sort(key=lambda x: x[1])
        return results

    def save(self):
        """Збереження книги контактів на диск у JSON форматі"""
        contacts_list = [record.to_dict() for record in self.data.values()]
        
        # Атомарне збереження через тимчасовий файл
        temp_file = self.data_file.with_suffix('.tmp')
        
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(contacts_list, f, ensure_ascii=False, indent=2)
            
            # Атомарна заміна
            temp_file.replace(self.data_file)
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            raise e

    def load(self):
        """Завантаження книги контактів з диска"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    contacts_list = json.load(f)
                
                self.data.clear()
                for contact_data in contacts_list:
                    record = Record.from_dict(contact_data)
                    self.data[record.name.value] = record
            except json.JSONDecodeError as e:
                print(f"⚠️  Помилка читання файлу даних: {e}")
                print("Створюється нова адресна книга")
                self.data.clear()
