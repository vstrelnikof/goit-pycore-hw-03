from dataclasses import dataclass
from .validator import Validator

@dataclass
class Contact:
    name: str
    phone: str
    email: str
    address: str
    birthday: str

    def __post_init__(self):
        self.phone = Validator.validate_phone(self.phone)
        self.email = Validator.validate_email(self.email)
        self.birthday = Validator.validate_date(self.birthday)

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.email} | {self.address} | {self.birthday}"