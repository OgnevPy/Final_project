import tkinter as tk
from tkinter import ttk
import sqlite3

# Создаем соединение с базой данных и курсор для выполнения SQL-запросов
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    email TEXT NOT NULL,
                    salary REAL NOT NULL)''')
conn.commit()

# Функция для добавления сотрудника в базу данных
def add_employee():
    full_name = entry_full_name.get()
    phone_number = entry_phone_number.get()
    email = entry_email.get()
    salary = entry_salary.get()

    # Проверяем, что все обязательные поля заполнены
    if not full_name or not phone_number or not email:
        result_label.config(text="Не все поля заполнены", foreground='red')
    else:
        # Вставляем данные в базу данных
        cursor.execute("INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)",
                   (full_name, phone_number, email, salary))
        conn.commit()
        result_label.config(text="Сотрудник добавлен успешно", foreground='green')
        clear_fields()
        display_employees()

# Функция для очистки полей ввода
def clear_fields():
    entry_full_name.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_salary.delete(0, tk.END)

# Функция для обновления данных сотрудника
def update_employee():
    selected_item = tree.focus()
    if selected_item:
        employee_id = tree.item(selected_item)['values'][0]
        new_name = entry_full_name.get()
        new_phone = entry_phone_number.get()
        new_email = entry_email.get()
        new_salary = entry_salary.get()

        if not new_name or not new_phone or not new_email:
            result_label.config(text="Не все поля заполнены", foreground='red')
        else:
            # Обновляем данные сотрудника в базе данных
            cursor.execute("UPDATE employees SET full_name=?, phone_number=?, email=?, salary=? WHERE id=?", 
                           (new_name, new_phone, new_email, new_salary, employee_id))
            conn.commit()
            result_label.config(text="Данные сотрудника обновлены успешно", foreground='green')
            clear_fields()
            display_employees()
    else:
        result_label.config(text="Выберите сотрудника для изменения", foreground='red')
    
# Функция для отображения сотрудников в таблице
def display_employees():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM employees")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# Функция для удаления сотрудника
def delete_employee():
    selected_item = tree.selection()
    if not selected_item:
        result_label.config(text="Выберите сотрудника для удаления", foreground='red')
    else:
        employee_id = tree.item(selected_item, "values")[0]
        cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        conn.commit()
        result_label.config(text="Сотрудник удален успешно", foreground='green')
        display_employees()

# Функция для поиска сотрудника
def search_employee():
    search_name = entry_search_name.get()
    # Использую символы подстановки % для поиска по частям ФИО
    cursor.execute("SELECT * FROM employees WHERE full_name LIKE ? OR full_name LIKE ? OR full_name LIKE ?",
                   ('%' + search_name, search_name + '%', '%' + search_name + '%'))
    results = cursor.fetchall()
    tree.delete(*tree.get_children())  # Очистить таблицу перед отображением результатов
    if results:
        for row in results:
            tree.insert("", "end", values=row)
        result_label.config(text=f"Найдено сотрудников: {len(results)}", foreground='green')
    else:
        result_label.config(text=f"Сотрудники с ФИО '{search_name}' не найдены", foreground='red')

# Создаем графический интерфейс
root = tk.Tk()
root.title("Список сотрудников компании")

# ограничение изменения размеров окна
root.resizable(False, False)

frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

# Окно для ввода ФИО
ttk.Label(frame, text="ФИО:").grid(row=0, column=0)
entry_full_name = ttk.Entry(frame)
entry_full_name.grid(row=0, column=1)

# Окно для ввода Номера телефона
ttk.Label(frame, text="Номер телефона:").grid(row=1, column=0)
entry_phone_number = ttk.Entry(frame)
entry_phone_number.grid(row=1, column=1)

# Окно для ввода адреса почты
ttk.Label(frame, text="Адрес почты:").grid(row=2, column=0)
entry_email = ttk.Entry(frame)
entry_email.grid(row=2, column=1)

# Окно для ввода зарплаты
ttk.Label(frame, text="Заработная плата:").grid(row=3, column=0)
entry_salary = ttk.Entry(frame)
entry_salary.grid(row=3, column=1)

# Кнопка добавить 
add_img = tk.PhotoImage(file='./img/add.png')
add_button = ttk.Button(frame, image=add_img, command=add_employee)
add_button.grid(row=4, column=0, columnspan=2)

# Кнопка изменить
update_img = tk.PhotoImage(file='./img/update.png')
update_button = ttk.Button(frame, image=update_img, command=update_employee)
update_button.grid(row=5, column=0, columnspan=2)

# Кнопка удалить
delete_img = tk.PhotoImage(file='./img/delete.png')
delete_button = ttk.Button(frame, image=delete_img, command=delete_employee)
delete_button.grid(row=6, column=0, columnspan=2)

# Окно для ввода поиска по ФИО
ttk.Label(frame, text="Поиск по ФИО:").grid(row=7, column=0)
entry_search_name = ttk.Entry(frame)
entry_search_name.grid(row=7, column=1)

# Кнопка найти
search_img = tk.PhotoImage(file='./img/search.png')
search_button = ttk.Button(frame, image=search_img, command=search_employee)
search_button.grid(row=8, column=0, columnspan=2)

# Окно для вывода текста
result_label = ttk.Label(frame, text="")
result_label.grid(row=9, column=0, columnspan=2)

# Таблица
tree = ttk.Treeview(frame, columns=("ID", "ФИО", "Телефон", "Почта", "Зарплата"), 
                        height=30, show='headings')
tree.heading("#1", text="ID")
tree.heading("#2", text="ФИО")
tree.heading("#3", text="Телефон")
tree.heading("#4", text="E-mail")
tree.heading("#5", text="Зарплата")
tree.grid(row=0, column=2, rowspan=10, padx=10, pady=10)
display_employees()

# Функция для обновления таблицы
def refresh_table():
    if result_label.cget("text") != "Таблица успешно обновлена":
        display_employees()
        result_label.config(text="Таблица успешно обновлена", foreground='green')

# Создание кнопки "Обновить таблицу" и привязка к функции refresh_table
refresh_button = ttk.Button(frame, text="Обновить таблицу", command=refresh_table)
refresh_button.grid(row=11, column=0, columnspan=2)

# Создание метки для отображения сообщения
result_label = ttk.Label(frame, text="")
result_label.grid(row=9, column=0, columnspan=2)

root.mainloop()

# Закрываем соединение с базой данных при выходе
conn.close()