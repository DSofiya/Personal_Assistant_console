import folium
import tkinter as tk
from tkinter import messagebox
import requests
import re
# from prompt_toolkit import prompt


def command_save(file_name, map_name):
    russia_map = folium.Map(location=[55.7558, 37.6176], zoom_start=5)

    with open(file_name, 'r') as file:
        for line in file:
            coordinates = line.strip().split(',')
            if len(coordinates) != 2:
                raise ValueError("Файл має містити координати,що складаються з двох чисел, розділені комою. Наприклад: 55.7558,37.6176")
            lat, lon = map(float, coordinates)

            folium.Marker(
                location=[lat, lon],
                icon=folium.DivIcon(
                    icon_size=(12, 12),
                    html='<div style="background-color: red; width: 12px; height: 12px;"></div>'
                ),
                tooltip=f'Координати: {lat}, {lon}'
            ).add_to(russia_map)

    russia_map.save(map_name)
    show_custom_message("Збереження координат", f"Мапа з  прапорцями збережена у файлі {map_name}.", 400, 200)

    

def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except UnboundLocalError:
            return "Неправильна назва міста."
        except ValueError:
            return "Incorrect date format."
    return wrapper


@input_error
def get_coordinates(city_name):
    api_key = "5cef6f4446b24817a8ebc8c727403c0a" 
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    
    params = { "q": city_name,"key": api_key}
    response = requests.get(base_url, params=params)
    data = response.json()
    if data.get("results") and data["results"][0]["geometry"]:
        lat = data["results"][0]["geometry"]["lat"]
        lng = data["results"][0]["geometry"]["lng"]
        coordinates = lat, lng
    
    if coordinates:
        show_custom_message("Пошук координат", f"Координати міста {city_name}: \n Широта: {lat} \n Довгота: {lng}", 400, 200)
    else:
        show_custom_message("Пошук координат", f"Не вдалося знайти координати для міста {city_name}.", 400, 200)



def check_coordinates(file_name, coordinates):
    with open(file_name, 'r') as file:
        existing_coordinates = file.readlines()
    if coordinates in existing_coordinates:
        return True
    else:
        return False


def add_coordinates(file_name, coordinates):
    if not check_coordinates(file_name, coordinates):
        pattern = r'^-?\d+(\.\d+)?,-?\d+(\.\d+)?$'
        if re.match(pattern, coordinates):
            with open(file_name, 'a') as file:
                file.write('\n'+ coordinates)
                show_custom_message("Додавання координат", f"Координати {coordinates} були додані до файлу.", 400, 200)
                
        else:
            show_custom_message("Додавання координат", f"Координати {coordinates} мають неправильний формат.", 400, 200)

    else:
        show_custom_message("Додавання координат", f"Координати {coordinates} вже існують у файлі.", 400, 200)


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
    root = tk.Tk()
    root.title("Мапа")

    def add_coordinates_nuclear_wrapper():
        input_str = entry.get()
        add_coordinates('Personal_assistant\Map\coordinates_nuclear.txt',input_str)
    
    def add_coordinates_air_wrapper():
        input_str = entry.get()
        add_coordinates('Personal_assistant\Map\coordinates_air.txt',input_str)
    
    def add_coordinates_admin_wrapper():
        input_str = entry.get()
        add_coordinates('Personal_assistant\Map\coordinates_admin.txt',input_str)

    def get_coordinates_wrapper():
        input_str = entry1.get()
        get_coordinates(input_str)

    def command_save_nuclear_wrapper():
        command_save('Personal_assistant\Map\coordinates_nuclear.txt','russia_map_nuclear.html')
    
    def command_save_air_wrapper():
        command_save('Personal_assistant\Map\coordinates_air.txt','russia_map_air.html')

    def command_save_admin_wrapper():
        command_save('Personal_assistant\Map\coordinates_admin.txt','russia_map_admin.html')

    root.geometry("600x700")

    button_width = 50
    button_height = 3

    tk.Label(root, text="Поле для введення нових координат.\nПриклад: 55.7558,37.6176 ").pack()
    entry = tk.Entry(root)
    entry.pack(pady=5)

    tk.Button(root, text="Зберегти мапу ядерних обєктів країни 404", width=button_width, height=button_height,command=command_save_nuclear_wrapper).pack(pady=5)
    tk.Button(root, text="Додати кординати до файлу з ядерними обєктами", width=button_width, height=button_height,command= add_coordinates_nuclear_wrapper).pack(pady=5)
    tk.Button(root, text="Зберегти мапу аеропортів країни 404", width=button_width, height=button_height,command=command_save_air_wrapper).pack(pady=5)
    tk.Button(root, text="Додати кординати до файлу з аеропортами", width=button_width, height=button_height,command= add_coordinates_air_wrapper).pack(pady=5)
    tk.Button(root, text="Зберегти мапу адмін обєктів країни 404", width=button_width, height=button_height,command=command_save_admin_wrapper).pack(pady=5)
    tk.Button(root, text="Додати кординати до файлу з адмін обєктами", width=button_width, height=button_height,command= add_coordinates_admin_wrapper).pack(pady=5)

    tk.Label(root, text="Поле для введення назви міст.\nПриклад: Москва").pack()
    entry1 = tk.Entry(root)
    entry1.pack(pady=5)

    tk.Button(root, text="Отримати кординати за назвою міста", width=button_width, height=button_height,
              command=get_coordinates_wrapper).pack(pady=5)
    tk.Button(root, text="Вихід у головне меню", width=button_width, height=button_height,
              command=root.destroy).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()