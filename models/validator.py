import re
from datetime import datetime

class Validator:
    @staticmethod
    def validate_phone(phone: str) -> str:
        if not re.match(r"^\+?\d{10,15}$", phone):
            raise ValueError("❌ Некоректний номер телефону!")
        return phone

    @staticmethod
    def validate_email(email: str) -> str:
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValueError("❌ Некоректний email!")
        return email

    @staticmethod
    def validate_date(date_str: str) -> str:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError("❌ Дата повинна бути у форматі YYYY-MM-DD")