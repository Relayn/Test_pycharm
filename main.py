import tkinter as tk
from tkinter import messagebox
import json

# Функция для добавления задачи в список
def add_task():
    task = task_entry.get()
    priority = priority_var.get()
    if task:
        # Добавление задачи в видимый список
        task_listBox.insert(tk.END, f"[{priority}] {task}")
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Ошибка", "Введите задачу!")

# Функция для удаления выбранной задачи из списка
def delete_task():
    selected_task = task_listBox.curselection()
    if selected_task:
        task_listBox.delete(selected_task)
        save_tasks()
    else:
        messagebox.showwarning("Ошибка", "Выберите задачу для удаления!")

# Функция для отметки выполненной задачи
def mark_task():
    selected_task = task_listBox.curselection()
    if selected_task:
        current_text = task_listBox.get(selected_task)
        # Пометка задачи как выполненной
        if not current_text.startswith("[✔] "):
            task_listBox.delete(selected_task)
            task_listBox.insert(selected_task, f"[✔] {current_text}")
            save_tasks()
        else:
            messagebox.showinfo("Информация", "Эта задача уже выполнена.")
    else:
        messagebox.showwarning("Ошибка", "Выберите задачу для отметки!")

# Функция для поиска задач
def search_task():
    keyword = search_entry.get().lower()
    if keyword:
        task_listBox.delete(0, tk.END)
        for task in tasks:
            task_text = f"[{task['priority']}] {task['name']}"
            if keyword in task['name'].lower():
                task_listBox.insert(tk.END, task_text)
                if task['completed']:
                    task_listBox.itemconfig(tk.END, bg="light green")
    else:
        load_tasks()

# Функция для сохранения задач в файл
def save_tasks():
    tasks.clear()
    for i in range(task_listBox.size()):
        task_text = task_listBox.get(i)
        completed = task_text.startswith("[✔]")
        # Убираем отметку "[✔]" из текста задачи
        if completed:
            task_text = task_text[4:]
        # Парсинг приоритета
        priority_end = task_text.find("]")
        priority = task_text[1:priority_end]
        task_name = task_text[priority_end + 2:]
        tasks.append({"name": task_name, "priority": priority, "completed": completed})
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

# Функция для загрузки задач из файла
def load_tasks():
    try:
        task_listBox.delete(0, tk.END)
        with open('tasks.json', 'r') as file:
            data = json.load(file)
            for task in data:
                task_text = f"[{task['priority']}] {task['name']}"
                task_listBox.insert(tk.END, task_text)
                if task['completed']:
                    task_listBox.itemconfig(tk.END, bg="light green")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

# Список задач
tasks = []

# Создание главного окна
root = tk.Tk()
root.title("Список задач")
root.configure(background="light blue")

# Метка для ввода задачи
text1 = tk.Label(root, text="Введите вашу задачу:", bg="light blue")
text1.pack(pady=5)

# Поле ввода для задачи
task_entry = tk.Entry(root, width=30, bg="white")
task_entry.pack(pady=10)

# Выпадающий список для выбора приоритета
priority_var = tk.StringVar(value="Средний")
priority_label = tk.Label(root, text="Приоритет:", bg="light blue")
priority_label.pack(pady=5)
priority_menu = tk.OptionMenu(root, priority_var, "Высокий", "Средний", "Низкий")
priority_menu.pack(pady=5)

# Кнопка для добавления задачи
add_task_button = tk.Button(root, text='Добавить задачу', command=add_task)
add_task_button.pack(pady=5)

# Кнопка для удаления задачи
delete_button = tk.Button(root, text='Удалить задачу', command=delete_task)
delete_button.pack(pady=5)

# Кнопка для отметки выполненной задачи
mark_button = tk.Button(root, text='Отметить выполненную задачу', command=mark_task)
mark_button.pack(pady=5)

# Поле ввода для поиска задач
search_entry = tk.Entry(root, width=30, bg="white")
search_entry.pack(pady=10)

# Кнопка для поиска задач
search_button = tk.Button(root, text='Поиск задачи', command=search_task)
search_button.pack(pady=5)

# Метка для списка задач
text2 = tk.Label(root, text="Список задач:", bg='light blue')
text2.pack(pady=5)

# Список задач
task_listBox = tk.Listbox(root, height=10, width=50, bg="white")
task_listBox.pack(pady=10)

# Загрузка задач при запуске приложения
load_tasks()

# Запуск главного цикла обработки событий
root.mainloop()
