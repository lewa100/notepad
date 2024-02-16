import csv
import os
import time
from datetime import datetime
from columnar import columnar

file = 'notes.csv'
row_number = 0

if not os.path.exists(file):
    open(file, 'w').close()
else:
    with open(file,'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=";")
        for s in reader:
            if int(s[0]) > row_number:
                row_number = int(s[0])

input_target_text = 'Введите вариант:'
input_row_number_copy_text = 'Введите ID строки для копирования:'
input_row_number_del_text = 'Введите ID строки для удаления:'
input_row_number_edit_text = 'Введите ID строки для изменениня:'
input_filter_date_text = 'Введите дату для фильтрации заметок. Формат(дд.мм.гггг):'
input_filter_id_text = 'Введите ID заметки:'

edit_title_text = 'Хотите изменить заголовок? (y/n):'
edit_msg_text = 'Хотите изменить текст заметки? (y/n):'

err_not_found = 'Ничего не найдено!'
err_empty_string = 'Вы ввели пустую строку!'
err_date_incorrect = "Не корректно введена дата! Формат(дд.мм.гггг)"

# NEW_ROW
input_title_text = 'Введите загаловок заметки:'
input_msg_text = 'Введите текст заметки:'

enter_position = lambda text:int(input(text))
clear_console = lambda: os.system('cls' if os.name == 'nt' else 'clear')
clear_space = lambda s: list(map(lambda s: s.strip(), s))
get_tt = lambda: int(time.time())
print_tt = lambda tt: time.strftime("%d.%m.%Y %H:%M:%S",time.localtime(int(tt))) if isinstance(tt, str) else time.strftime("%d.%m.%Y %H:%M:%S",time.localtime(tt))

def print_tab(data, msg = f"\n############ Список заметок ############"):
    if len(data)<1:
        print(err_not_found)
        return
    for i, s in enumerate(data):
        data[i][-1] = print_tt(s[-1])
    headers = ['ID', 'Заголовок', 'Заметка', 'Дата/время']
    table = columnar(data, headers, no_borders=True)
    print(msg)
    print(table)

def get_new_row_id():
    global row_number
    row_number += 1
    return row_number


def enter_new_row():
    title = enter_text(input_title_text)
    note = enter_text(input_msg_text)
    row = [get_new_row_id(), title, note, get_tt()]
    print("\n\t\t----====Новая запись====----")
    write_row_to_file(row)
    print_tab([row])
    print()
    input("Press Enter to continue...")
def enter_text(text):
    while True:
        try:
            s = input(text)
            if (s == ""):
                raise KeyboardInterrupt
            return s
        except KeyboardInterrupt:
            print(err_empty_string)
            continue

def enter_date(text):
    while True:
        try:
            date_text = enter_text(text)
            return datetime.strptime(date_text, "%d.%m.%Y")
        except ValueError:
            print(err_date_incorrect)
            continue

def str_tt_to_date(date_text):
    try:
        return datetime.utcfromtimestamp(int(date_text))
    except ValueError:
        raise ValueError(err_date_incorrect)

def enter_position(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print('Введите корректно число!')
            continue

def print_menu():
    clear_console()
    print("\n\t\t----====МЕНЮ====----")
    print(f"1.\t Добавить новую заметку")
    print(f"2.\t Удалить заметку по ID")
    print(f"3.\t Изменить заметку по ID")
    print(f"4.\t Распечатать весь список заметок")
    print(f"5.\t Распечатать список заметок по дате создания/изменения")
    print(f"6.\t Распечатать заметку по ID")

    print("9.\t Выход\n")

def print_file(file):
    data = []
    with open(file,'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=";")
        for s in reader:
            s = clear_space(s)
            data.append(s)
    print_tab(data, f"\n############ Список заметок из файла ############")
    print()
    input("Press Enter to continue...")

def find_rows_by_filter(column_name,filter):
    column_number = 0
    if (column_name.lower() == "date"):
        column_number = 3
    rows = []
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=";")
        for line in reader:
            if column_name == "date":
                try:
                    tt_line = str_tt_to_date(line[column_number])
                    if tt_line.date() == filter.date():
                        rows.append(clear_space(line))
                except ValueError as error:
                    print(error)
                    break
            else:
                if (line[column_number] == str(filter)):
                    rows.append(clear_space(line))
    return rows

def del_row(num):
    row_list = []
    find = False
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=";")
        for line in reader:
            if line[0] == str(num):
                find = True
                continue
            row_list.append(line)
        if find:
            with (open(file, 'w', encoding='utf-8') as f):
                writer = csv.writer(f, delimiter=";")
                for r in row_list:
                    writer.writerow(r)


def edit_row_menu(num):
    row = find_rows_by_filter("id", num)
    if len(row) < 1:
        print(err_not_found)
        print()
        input("Press Enter to continue...")
        return
    print_tab(row, f"\n############ Запись для изменнения ############")

    answer = enter_text(edit_title_text)
    if answer.lower() == 'y':
        row[0][1] = enter_text(input_title_text)
        row[0][3] = get_tt()
    answer = enter_text(edit_msg_text)
    if answer.lower() == 'y':
        row[0][2] = enter_text(input_msg_text)
        row[0][3] = get_tt()
    print("\n\t\t----====Новая запись====----")
    edit_row(row[0])
    print_tab(row)
    print()
    input("Press Enter to continue...")

def edit_row(row):
    row_list = []
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=";")
        for line in reader:
            if line[0] == str(row[0]):
                row_list.append(row)
                continue
            row_list.append(line)
    with (open(file, 'w', encoding='utf-8') as f):
        writer = csv.writer(f, delimiter=";")
        for r in row_list:
            writer.writerow(r)

def write_row_to_file(s):
    with (open(file, 'a', encoding='utf-8') as f):
        writer = csv.writer(f,delimiter=";")
        writer.writerow(s)

target = 0
while (target!=9):
    print_menu()
    target = enter_position(input_target_text)
    if target == 1:
        enter_new_row()
    elif target == 2:
        n = enter_position(input_row_number_del_text)
        del_row(n)
        print_file(file)
    elif target == 3:
        n = enter_position(input_row_number_edit_text)
        edit_row_menu(n)
    elif target == 4:
        print_file(file)
    elif target == 5:
        filter = enter_date(input_filter_date_text)
        print_tab(find_rows_by_filter("date",filter),'############ Список отфильтрованный по дате ############')
        print()
        input("Press Enter to continue...")
    elif target == 6:
        filter = enter_position(input_filter_id_text)
        print_tab(find_rows_by_filter("id", filter),'############ Список отфильтрованный по ID ############')
        print()
        input("Press Enter to continue...")

    elif target != 9:
        print('Введите корректно пункт меню!')
        input("Press Enter to continue...")

