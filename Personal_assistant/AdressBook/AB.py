import tkinter as tk
from tkinter import messagebox
from collections import UserDict
from datetime import datetime, timedelta
import os
import sys
from dateutil.parser import parse
import dill as pickle
import re


from prompt_toolkit import prompt

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
            obj_datetime = parse(value).date()
            return obj_datetime
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

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def update_record(self, record: Record):
         self.data[record.name.value] = record

    def delete_record(self, record: Record):
        self.data.pop(record)

    def find_record(self, name):
        return self.data.get(name)

    def __init__(self):
        self.file_path = 'AdressBook.bin'
        super().__init__()

    def dump(self):
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def load(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, 'rb') as file:
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


def add_contact():
    def save_contact():
        name = name_entry.get()
        phone = phone_entry.get()
        birthday = birthday_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        new_contact = Record(Name(name), Phone(phone), Birthday(birthday), Email(email), Adress(address))
        contact_list.add_record(new_contact)
        add_window.destroy()
        messagebox.showinfo("Success", f"Contact {name} has been added.")

    add_window = tk.Toplevel()
    add_window.geometry("400x500")
    add_window.title("Add Contact")

    tk.Label(add_window, text="Ім'я:").pack(pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="Номер телефону:").pack(pady=5)
    phone_entry = tk.Entry(add_window)
    phone_entry.pack()

    tk.Label(add_window, text="День народження:").pack(pady=5)
    birthday_entry = tk.Entry(add_window)
    birthday_entry.pack()

    tk.Label(add_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(add_window)
    email_entry.pack()

    tk.Label(add_window, text="Адреса:").pack(pady=5)
    address_entry = tk.Entry(add_window)
    address_entry.pack()

    tk.Button(add_window, text="OK", command=save_contact).pack()


@input_error
def command_delete(input_str):
    result = contact_list.find_record(input_str)
    if result:
        contact_list.delete_record(result)
        show_custom_message("Delete ", f'Contact {input_str} succefully deleted', 800, 300)
  

def command_change():
    def update_record():
        name = name_entry.get()
        phone = phone_entry.get()
        birthday = birthday_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        update = Record(Name(name), Phone(phone), Birthday(birthday), Adress(email), Adress(address))
        contact_list.update_record(update)
        add_window.destroy()
        messagebox.showinfo("Success", f"Contact {name} has been changed.")

    add_window = tk.Toplevel()
    add_window.geometry("400x500")
    add_window.title("CЗмінити контакт")

    tk.Label(add_window, text="Ім'я:").pack(pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="Новий номер:").pack(pady=5)
    phone_entry = tk.Entry(add_window)
    phone_entry.pack()

    tk.Label(add_window, text="Нова дата народження:").pack(pady=5)
    birthday_entry = tk.Entry(add_window)
    birthday_entry.pack()

    tk.Label(add_window, text="Новий email:").pack(pady=5)
    email_entry = tk.Entry(add_window)
    email_entry.pack()

    tk.Label(add_window, text="Нова адреса:").pack(pady=5)
    address_entry = tk.Entry(add_window)
    address_entry.pack()

    tk.Button(add_window, text="OK", command=update_record).pack()


@input_error
def command_search(input_str):
    result = contact_list.find_record(input_str)
    if result:
        result = '{:<14}|{:^16}|{:^18}|{:^30}|{:^30} |\n'.format(result.name.value, result.phone.value, str(result.birthday.value), result.email.value, result.adress.value)   
        show_custom_message("Show ", result, 800, 300)



def show_all():
    result = ""
    if not contact_list:
        result = "List of contacts is empty"
    else:
        result += "Contacts:\n"
        result += 'Name          |     Number     |     Birthday     |            Email             |             Adress            |\n'
        for name, value in contact_list.items():
            result += '--------------|----------------|------------------|------------------------------|-------------------------------|\n'
            result += '{:<14}|{:^16}|{:^18}|{:^30}|{:^30} |\n'.format(name, value.phone.value, str(value.birthday.value), value.email.value, value.adress.value)

    show_custom_message("Show All", result, 800, 300)


@input_error
def days_to_birthday(days):
    result = ""
    d_now = datetime.now().date()
    for key, value in contact_list.items():
        birthday = value.birthday.value
        birthday = birthday.replace(year=d_now.year)
        days_to_br = timedelta(days=int(days))
        days_to_br = d_now + days_to_br
        if d_now <= birthday <= days_to_br:
            result += f'{key} have birthday in next {days} days. {value.birthday}\n'
    if not result:
        result = f'No birthdays in next {days} days'
    
    show_custom_message("days to birthday", result, 300, 200)


def show_custom_message(title, message, width, height):
    root = tk.Tk()
    root.withdraw() 
    custom_message = tk.Toplevel(root)
    custom_message.title(title)
    custom_message.geometry(f"{width}x{height}")
    label = tk.Label(custom_message, text=message)
    label.pack()
    ok_button = tk.Button(custom_message, text="OK", command=custom_message.destroy)
    ok_button.pack()
    custom_message.mainloop()
 

def main():
    if os.path.exists('AdressBook.bin'):
        contact_list.load()

    root = tk.Tk()
    root.title("Записник контактів")
    
    def command_search_wrapper():
        input_str = entry.get() 
        command_search(input_str)

    def command_delete_wrapper():
        input_str = entry.get() 
        command_delete(input_str)

    def days_to_birthday_wrapper():
        input_str = entry.get() 
        days_to_birthday(input_str)

    root.geometry("400x500")

    button_width = 20  
    button_height = 2
    
    tk.Label(root, text="Введіть ім'я для пошуку або видалення: ").pack()
    entry = tk.Entry(root)
    entry.pack(pady=5)
    
    tk.Button(root, text="Додати новий запис", width=button_width, height=button_height, command=add_contact).pack(pady=5)
    tk.Button(root, text="Змінити запис", width=button_width, height=button_height, command=command_change).pack(pady=5)
    tk.Button(root, text="Видалити запис", width=button_width, height=button_height, command=command_delete_wrapper).pack(pady=5)
    tk.Button(root, text="Знайти запис", width=button_width, height=button_height, command=command_search_wrapper).pack(pady=5)
    tk.Button(root, text="Показати всі", width=button_width, height=button_height, command=show_all).pack(pady=5)
    tk.Button(root, text="Днів до дня народження", width=button_width, height=button_height, command=days_to_birthday_wrapper).pack(pady=5)
    tk.Button(root, text="Вихід у головне меню", width=button_width, height=button_height, command=root.destroy).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

