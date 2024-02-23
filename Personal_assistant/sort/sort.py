import os
import shutil
import tkinter as tk
from tkinter import messagebox

class FileSorter:
    def __init__(self, path):
        self.path = path
        self.extensions = {
            'images': ('.jpg', '.png', '.jpeg', '.svg'),
            'videos': ('.avi', '.mp4', '.mov', '.mkv'),
            'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
            'music': ('.mp3', '.ogg', '.wav', '.amr'),
            'archives': ('.zip', '.gz', '.tar'),
            'python' : ('.py')
        }

        self.unknown_extensions = set()

        self.for_print = {
            'images': [],
            'videos': [],
            'documents': [],
            'music': [],
            'archives': [],
            'python' : []
        }

    def normalize(self, name):
        return ''.join(c for c in name if c.isalnum() or c in [' ', '.', '_']).rstrip()


    def add_and_print_extensions(self, folder, extension):
        if folder in self.for_print:
            if extension not in self.for_print[folder]:
                self.for_print[folder].append(extension)
        else:
            self.unknown_extensions.add(extension)


    def sort_files(self):
        for root, dirs, files in os.walk(self.path):
            for folder in dirs:
                if folder.lower() in self.extensions.keys():
                    dirs.remove(folder)

            for file in files:
                filename, extension = os.path.splitext(file)
                found = False
                for folder, exts in self.extensions.items():
                    if extension.lower() in exts:
                        new_path = os.path.join(root, folder, self.normalize(file))
                        os.makedirs(os.path.dirname(new_path), exist_ok=True)
                        shutil.move(os.path.join(root, file), new_path)
                        found = True
                        self.add_and_print_extensions(folder, extension.lower())
                        break
                if not found:
                    self.unknown_extensions.add(extension.lower())

        for folder in ['archives']:
            for root, dirs, files in os.walk(os.path.join(self.path, folder)):
                for file in files:
                    filename, extension = os.path.splitext(file)

                    if extension.lower() in self.extensions['archives']:
                        self.for_print['archives'].append(extension.lower())

                    if extension.lower() == '.zip':
                        new_folder = os.path.join(root, self.normalize(filename))
                        os.makedirs(new_folder, exist_ok=True)
                        shutil.unpack_archive(os.path.join(root, file), new_folder)
                        os.remove(os.path.join(root, file))

    def print_results(self):
        print('Знайдені розширення:')
        for folder, extensions in self.for_print.items():
            if extensions:
                print(f'{folder}: {", ".join(extensions)}')
        
        print('Невідомі розширення:')
        print(', '.join(self.unknown_extensions))
    



def main():

    def  start_sort_files():
        input_str = entry.get() 
        path = str(input_str)
        if path == '' or path == 'cancel':
            messagebox.showinfo("Success", "You have unsorted")
            add_window.destroy()
        else:
            sorter = FileSorter(path)
            sorter.sort_files()
            sorter.print_results()
            messagebox.showinfo("Success", "You have sorted all file")
            add_window.destroy()

    add_window = tk.Toplevel()
    add_window.geometry("400x500")
    add_window.title("Для відміни введіть пусту строку або cancel")
    tk.Label(add_window, text="Шлях до папки ==> (C:|Users|Oleg|Documents|some_rubbish): ").pack()
    entry = tk.Entry(add_window)
    entry.pack()
    tk.Button(add_window, text="OK", command=start_sort_files).pack()
    
    

if __name__ == "__main__":
    main()