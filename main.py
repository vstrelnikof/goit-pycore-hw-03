from datetime import datetime, timedelta
import random
import re

def get_days_from_today(date: str) -> int:
    try:
        # Перетворюємо рядок у дату
        given_date = datetime.strptime(date, "%Y-%m-%d").date()
        # Отримуємо поточну дату
        today = datetime.today().date()
        # Різниця у днях
        delta = today - given_date
        return delta.days
    except ValueError as e:
        print("Неправильний формат дати. Використовуйте 'YYYY-MM-DD'.")
        raise e

def get_numbers_ticket(min: int, max: int, quantity: int) -> list:
    # Перевірка коректності параметрів
    if min < 1 or max > 1000 or quantity > (max - min + 1) or quantity <= 0:
        return []
    # Генеруємо унікальні випадкові числа
    numbers = random.sample(range(min, max + 1), quantity)
    # Повертаємо відсортований список
    return sorted(numbers)

def normalize_phone(phone_number: str) -> str:
    # Видаляємо зайві пробіли на початку та в кінці
    phone_number = phone_number.strip()
    # Залишаємо тільки цифри та символ '+'
    phone_number = re.sub(r"[^\d+]", "", phone_number)
    # Якщо номер починається з '+', перевіряємо чи є код країни
    if phone_number.startswith("+"):
        # Якщо після '+' йде '38', залишаємо як є
        if phone_number.startswith("+38"):
            return phone_number
        # Якщо після '+' йде '380', теж залишаємо як є
        elif phone_number.startswith("+380"):
            return phone_number
        # Інакше повертаємо як є (може бути інший міжнародний код)
        else:
            return phone_number
    else:
        # Якщо номер починається з '380', додаємо '+'
        if phone_number.startswith("380"):
            return "+" + phone_number
        # Якщо номер починається з '0' або іншої цифри — додаємо '+38'
        else:
            return "+38" + phone_number

def get_upcoming_birthdays(users):
    today = datetime.today().date()
    upcoming_birthdays = []
    for user in users:
        # Перетворюємо дату народження у формат datetime.date
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        # День народження цього року
        birthday_this_year = birthday.replace(year=today.year)
        # Якщо день народження вже минув цього року — беремо наступний рік
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        # Різниця у днях
        delta_days = (birthday_this_year - today).days
        # Перевіряємо, чи день народження у межах наступних 7 днів
        if 0 <= delta_days <= 7:
            congratulation_date = birthday_this_year
            # Якщо день народження припадає на вихідний (субота або неділя)
            if congratulation_date.weekday() == 5: # субота
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6: # неділя
                congratulation_date += timedelta(days=1)
            # Додаємо у список результатів
            upcoming_birthdays.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })
    return upcoming_birthdays

if __name__ == "__main__":
    # Тестуємо get_days_from_today
    date_input = input("Введіть дату у форматі 'YYYY-MM-DD': ")
    days = get_days_from_today(date_input)
    print(f"Кількість днів від введеної дати до сьогодні: {days}")
    # Тестуємо get_numbers_ticket
    lottery_numbers = get_numbers_ticket(1, 49, 6)
    print("Ваші лотерейні числа:", lottery_numbers)
    # Тестуємо normalize_phone
    raw_numbers = [
        "067\t123 4567",
        "(095) 234-5678\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
    ]
    sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
    print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)
    # Тестуємо get_upcoming_birthdays
    users = [
        {"name": "John Doe", "birthday": "1985.02.8"},
        {"name": "Jane Smith", "birthday": "1990.02.14"},
        {"name": "Alex Johnson", "birthday": "1992.02.25"},
    ]
    upcoming_birthdays = get_upcoming_birthdays(users)
    print("Список привітань на цьому тижні:", upcoming_birthdays)
