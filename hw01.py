""""
    Розробіть систему для управління адресною книгою.

    Сутності:

    Field: Базовий клас для полів запису.
    Name: Клас для зберігання імені контакту. Обов'язкове поле.
    Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    AddressBook: Клас для зберігання та управління записами.


    Функціональність:

    AddressBook:Додавання записів.
    Пошук записів за іменем.
    Видалення записів за іменем.
    Record:Додавання телефонів.
    Видалення телефонів.
    Редагування телефонів.
    Пошук телефону.
"""

from collections import UserDict


class Field:
    """Base class for fields."""
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
    
class Name(Field):
    """Class representing a name field."""
    pass

class Phone(Field):
    """Class representing a phone number field."""
    def __init__(self, value: str):
        if not isinstance(value, str) or len(value) != 10 or not value.isdigit():
            raise ValueError(f"Phone number {value} must be a string of 10 digits.")
        super().__init__(value)

class Record:
    """Class representing a record with a name and phone numbers."""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {';'.join(str(p) for p in self.phones)}"
    
    def add_phone(self, phone: str) -> None:
        """Add a phone number to the record."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Remove a phone number from the record."""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit a phone number in the record."""
        if not self.find_phone(old_phone):
            raise ValueError(f"The phone number to edit '{old_phone}' doesn't exist.")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)     

    def find_phone(self, phone: str) -> Phone:
        """Find a phone number in the record."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

class AddressBook(UserDict):
    """Class representing an address book."""
    def add_record(self, record: Record) -> None:
        """Add a record to the address book."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """Find a record in the address book by name."""
        return self.data.get(name, f"The name '{name}' doesn't exist.")
    
    def delete(self, name: str) -> Record:
        """Delete a record from the address book by name."""
        return self.data.pop(name, f"There is no such name as '{name}' in the address book.")
      
# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення записів
deleted_jane = book.delete("Jane")
does_not_exist = book.delete("Jack")
print(deleted_jane)
print(does_not_exist)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)
