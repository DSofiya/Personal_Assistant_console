import os
import tkinter as tk
from AdressBook.AB import main as ab_main
from Map.Map import main as map_main
from sort.sort import main as sort_main
from Game.game import main as game_main

def cls():
    os.system(['clear', 'cls'][os.name == 'nt'])

def menu():
    cls()

    root = tk.Tk()
    root.title("Personal Assistant")
    root.geometry("400x500")
    
    def open_ab():
        ab_main()

    def open_map():
        map_main()

    def open_sort():
        sort_main()

    def open_game():
        game_main()

    button_width = 20
    button_height = 2

    
    tk.Button(root, text="Записна книжка", width=button_width, height=button_height, command=open_ab).pack(pady=5)
    tk.Button(root, text="Карта", width=button_width, height=button_height, command=open_map).pack(pady=5)
    tk.Button(root, text="Сортування папки", width=button_width, height=button_height, command=open_sort).pack(pady=5)
    tk.Button(root, text="Гра", width=button_width, height=button_height, command=open_game).pack(pady=5)
    tk.Button(root, text="Вихід", width=button_width, height=button_height, command=root.destroy).pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    menu()