from collections import UserDict
from datetime import datetime, timedelta
import os
import dill as pickle
import re
from dateparser import parse
from prompt_toolkit import prompt
from .prompt_tool import Completer, RainbowLetter


class Field:
    def __init__(self, some_value):
        self._value = None
        self.value = some_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return f'{self.value}'


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        for i in value:
            if i.isdigit() or i in '+()':
                continue
            else:
                raise TypeError
        self._value = value


class Birthday(Field):
    def valid_date(self, value: str):
        try:
            # obj_datetime = parse(value)
            obj_datetime = datetime.strptime(value, '%Y-%m-%d')
            return obj_datetime.date()
        except KeyError:
            raise TypeError('Wrong data type. Try "yyyy-mm-dd"')

    @Field.value.setter
    def value(self, value):
        self._value = self.valid_date(value)


class Email(Field):
    @Field.value.setter
    def value(self, value: str):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, value):
            self._value = value
        else:
            raise TypeError(f'Wrong email')


class Adress(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone, birthday: Birthday, email: Email, adress=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
            self.phone = phone
        self.birthday = birthday
        self.email = email
        if adress:
            self.adress = adress

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def remove_phone(self, phone):
        phone_obj = Phone(phone)
        if phone_obj in self.phones:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def days_to_birthday(self):
        pass


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def update_record(self, record: Record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        self.data.pop(name)

    def find_record(self, name):
        return self.data.get(name)

    def __init__(self):
        super().__init__()

    def dump(self):
        with open('AdressBook.bin', 'wb') as file:
            pickle.dump(self.data, file)

    def load(self):
        with open('AdressBook.bin', 'rb') as file:
            self.data = pickle.load(file)
        
contact_list = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "ValueError. Try again"
        except IndexError:
            return "IndexError. Try again"
        except NameError:
            return "Invalid input. Name should contain only letters."
        except TypeError:
            return "Invalid input. Try again"
    return wrapper


# @input_error
def command_add():
    name = Name(input("Введіть ім'я: ").title())
    phone = Phone(input('Введіть номер: '))
    birthday = Birthday(input('Введіть дату народження: '))
    email = Email(input('Введіть email-пошту: '))
    adress = Adress(input('Введіть адрессу: '))
    contacts = Record(name, phone, birthday, email, adress)
    contact_list.add_record(contacts)
    return f"Contact {name} has been added."


@input_error
def command_delete(input_str):
    _, name = input_str.split()
    contact_list.delete_record(name.title())
    return f'Contact {name.title()} succefully deleted'


@input_error
def command_change():
    name = Name(input("Введіть ім'я: ").title())
    phone = Phone(input('Введіть номер: '))
    birthday = Birthday(input('Введіть дату народження: '))
    email = Email(input('Введіть email-пошту: '))
    adress = Adress(input('Введіть адрессу: '))
    update = Record(name, phone, birthday, email, adress)
    contact_list.update_record(update)
    return f"Contact {name} has been updated."


@input_error
def command_search(input_str):
    _, name = input_str.split()
    result = contact_list.find_record(name.title())
    return result.name.value, result.phone.value, str(result.birthday.value), result.email.value, result.adress.value


def command_show_all(contact_list):
    if not contact_list:
        return "Список контактів пустий."
    result = "Contacts:"
    print(result)
    print('------------------------------------------------------------------------------------------------------------------')
    print('Name          |     Number     |     Birthday     |            Email             |             Adress            |')
    for name, value in contact_list.items():
        print('--------------|----------------|------------------|------------------------------|-------------------------------|')
        print('{:<14}|{:^16}|{:^18}|{:^30}|{:^30} |'.format(name, value.phone.value, str(
            value.birthday.value), value.email.value, value.adress.value))
    print('------------------------------------------------------------------------------------------------------------------')


@input_error
def command_days_to_birthday(input_str):
    result = ''
    _, days = input_str.split()
    d_now = datetime.now().date()
    for key, value in contact_list.items():
        birthday = value.birthday.value
        birthday = birthday.replace(year=d_now.year)
        days_to_br = timedelta(days=int(days))
        days_to_br = d_now + days_to_br
        if d_now <= birthday <= days_to_br:
            result += f'{key} have birthday in next {days} days. {value.birthday}\n'
        else:
            continue
    return result.strip() if result else f'No birthdays in next {days} days'

def main():
    if os.path.exists('AdressBook.bin'):
        contact_list.load()
    print("Доступні команди:'hello','add','change', 'delete', 'search', 'birthday', 'show all','good bye','close','exit'")
    while True:
        input_str = prompt("Enter your command: ",completer=Completer, lexer=RainbowLetter())

        if input_str == "hello":
            print("How can I help you?")
        elif input_str.startswith("add"):
            print(command_add())
        elif input_str.startswith("change"):
            print(command_change())
        elif input_str.startswith("delete "):
            print(command_delete(input_str))
        elif input_str.startswith("search "):
            print(command_search(input_str))
        elif input_str.startswith("birthday "):
            print(command_days_to_birthday(input_str))
        elif input_str == "show all":
            command_show_all(contact_list)
        elif input_str in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Невірно введена команда. Доступні команди:'hello','add','change','phone','show all','good bye','close','exit'")
        contact_list.dump()


if __name__ == "__main__":
    main()

