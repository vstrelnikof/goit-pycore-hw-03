"""
Моделі для адресної книги
"""
from datetime import datetime, date
import re


class Field:
    """Базовий клас для полів запису"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту"""
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Ім'я не може бути порожнім")
        super().__init__(value)


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією"""
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Некоректний номер телефону. Використовуйте формат: 10 цифр")
        super().__init__(value)
    
    @staticmethod
    def validate(phone):
        """Валідація номера телефону (10 цифр)"""
        pattern = r'^\d{10}$'
        return bool(re.match(pattern, phone))


class Email(Field):
    """Клас для зберігання email з валідацією"""
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Некоректний email")
        super().__init__(value)
    
    @staticmethod
    def validate(email):
        """Валідація email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


class Birthday(Field):
    """Клас для зберігання дня народження"""
    def __init__(self, value):
        if isinstance(value, str):
            try:
                self.value = datetime.strptime(value, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError("Некоректна дата. Використовуйте формат: DD.MM.YYYY")
        elif isinstance(value, date):
            self.value = value
        else:
            raise ValueError("Некоректний тип даних для дня народження")


class Address(Field):
    """Клас для зберігання адреси"""
    pass


class Record:
    """Клас для зберігання інформації про контакт"""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None

    def add_phone(self, phone):
        """Додавання телефону"""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Видалення телефону"""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """Редагування телефону"""
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Телефон не знайдено")

    def find_phone(self, phone):
        """Пошук телефону"""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_email(self, email):
        """Додавання email"""
        self.email = Email(email)

    def add_birthday(self, birthday):
        """Додавання дня народження"""
        self.birthday = Birthday(birthday)

    def add_address(self, address):
        """Додавання адреси"""
        self.address = Address(address)

    def days_to_birthday(self):
        """Розрахунок днів до наступного дня народження"""
        if not self.birthday:
            return None
        
        today = datetime.now().date()
        birthday_this_year = self.birthday.value.replace(year=today.year)
        
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        
        delta = birthday_this_year - today
        return delta.days

    def to_dict(self):
        """Серіалізація контакту в словник для JSON"""
        return {
            'name': self.name.value,
            'phones': [phone.value for phone in self.phones],
            'email': self.email.value if self.email else None,
            'birthday': self.birthday.value.strftime('%d.%m.%Y') if self.birthday else None,
            'address': self.address.value if self.address else None
        }
    
    @staticmethod
    def from_dict(data):
        """Десеріалізація контакту зі словника JSON"""
        record = Record(data['name'])
        
        for phone in data.get('phones', []):
            record.add_phone(phone)
        
        if data.get('email'):
            record.add_email(data['email'])
        
        if data.get('birthday'):
            record.add_birthday(data['birthday'])
        
        if data.get('address'):
            record.add_address(data['address'])
        
        return record

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        result = f"Контакт: {self.name.value}"
        if phones_str:
            result += f", телефони: {phones_str}"
        if self.email:
            result += f", email: {self.email.value}"
        if self.birthday:
            result += f", день народження: {self.birthday.value.strftime('%d.%m.%Y')}"
        if self.address:
            result += f", адреса: {self.address.value}"
        return result
