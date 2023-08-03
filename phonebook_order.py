from pprint import pprint
import csv
import re
# Читаем адресную книгу в формате CSV в список contacts_list:
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    #pprint(contacts_list)

def name_correction(rows): # Объединяем через пробел колонки ФИО и затем разъединяем их, чтобы привести в порядок данные таким образом, чтобы Ф, И, О падали в отдельные колонки
    result = [' '.join(employee[0:3]).split(' ')[0:3] + employee[3:7] for employee in rows]
    return result

def drop_duplicates(correct_name_list): # Удаляем дубликаты, если таковые имеются
    no_duplicates = []
    for compared in correct_name_list:
        for employee in correct_name_list:
            if compared[0:2] == employee[0:2]:
                list_employee = compared
                compared = list_employee[0:2]
                for i in range(2, 7):
                    if list_employee[i] == '':
                        compared.append(employee[i])
                    else:
                        compared.append(list_employee[i])
        if compared not in no_duplicates:
            no_duplicates.append(compared)

    return no_duplicates

def updating_phone_numbers(rows, regular, new): # Приводим в порядок номера с учетом добавочного
    phonebook = []
    pattern = re.compile(regular)
    phonebook = [[pattern.sub(new, string) for string in strings] for strings in rows]

    return phonebook

correct_name_list = name_correction(contacts_list)
no_duplicates_list = drop_duplicates(correct_name_list)
regular = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})' # Номер телефона
correct_list = updating_phone_numbers(no_duplicates_list, regular, r'+7(\2)\3-\4-\5')
regular_2 = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s]*[(доб.\s]*(\d+)[)]*' # Номер телефона с добавочным
correct_phonebook = updating_phone_numbers(correct_list, regular_2, r'+7(\2)\3-\4-\5 доб.\6')

with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(correct_phonebook)