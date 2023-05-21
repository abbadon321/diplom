group = "02.03.02|7471|ИМИ-Б-ФИИТ-21|5998"
print(group[3:5])

# from bs4 import BeautifulSoup
# import requests

# def parse_addrow(html, lecturer):
#     soup = BeautifulSoup(html, 'html.parser')
#     options = soup.find_all('option')

#     surname, initials = lecturer.split()
#     initials = initials.replace(".", "")

#     for option in options:
#         text = option.text
#         if text.startswith(surname):
#             string = text.split()
#             lecturer_initials = string[1][0] + string[2][0]
#             if initials == lecturer_initials:
#                 return text + "|" + option['value']

#     else:
#         # есть проблема совпадений по фамилии и инициалам а также полных тесок
#         response = requests.get(
#             url=f"https://www.s-vfu.ru/stud/searchadddata.php?tablename=svfudbnew.forexcel&term={surname} {initials[0]}")
#         data = response.json()
#         for d in data:
#             string = d.split()
#             if string[2].startswith(initials[1]):
#                 return d
#             else: "Преподаватель не найден!"


# html = '<select name="hours"><option value=""></option><option value="895038073">Акимов Федор Револьевич</option><option value="714069">Алексеев Николай Кириллович</option><option value="90258224">Божевольная Зоя Анатольевна</option><option value="895038074">Варламова Анастасия Гаврииловна</option><option value="895035721">Васильева Лира Петровна</option><option value="895035612">Габышева Анна Михайловна</option><option value="895038096">Герасимов Георгий Егорович</option><option value="895038199">Голоков Вячеслав Валерьевич</option><option value="717477">Дедюкина Любовь Лукинична</option><option value="717689">Донская Маргарита Ивановна</option><option value="718121">Егорова Валентина Никифоровна</option><option value="219536635">Ефимова Кристина Семеновна</option><option value="718509">Жафяров Акрям Жафярович</option></select>'
# lecturer = "Попов В.В."

# print(parse_addrow(html, lecturer))

# lecturer = "Акинин Михаил Александрович|895035670"
# print(lecturer[lecturer.find("|") + 1:])

# from openpyxl import load_workbook
# import re

# wb = load_workbook(filename='C:\\Users\\user\\Documents\\GitHub\\diplom\\flask\\static\\тест.xlsx')
# sheets_names = wb.sheetnames
# wb.active = sheets_names.index("1 курс_МО")
# ws = wb.active
# print(ws.title)
# text = str(ws.cell(row=27, column=4).value).split("\n")
# print(text)
# s = None
# if str(s) == "None":
#     print("yes")


# def extract_word(string):
#     # Паттерн для поиска числа и слова
#     pattern = r'\b(\d+)\b\s+([a-zA-Zа-яА-Я]{2,})\b'
    
#     # Ищем совпадения в строке
#     match = re.search(pattern, string)
    
#     if match is not None:
#         # Возвращаем слово из совпадения
#         return match.group(2)
#     else:
#         return None

# # цикл по листам excel-файла
# for sh in sheets_names:
#     wb.active = sheets_names.index(sh)
#     ws = wb.active
#     print("\n", ws.title)
#     text = str(ws.cell(row=3, column=6).value).split("\n")
#     print(text)
#     for i in range(6, ws.max_column, 4):
#         for j in range(6, 42):
#             if ws.cell(row=j, column=i).value is not None:
#                 string = str(ws.cell(row=j, column=i).value)
#                 result = extract_word(string) if (result := extract_word(string)) is not None else "КФЕН"
#                 print(result, end=", ")

                
            # if str(ws.cell(row=j, column=i).value).find("*,**") != -1:
            # if str(ws.cell(row=j, column=i).value).find("*") != -1:
            #     print(ws.cell(row=j, column=i).value)
            #     print( (ws.cell(row=j, column=i).value.strip()))
            #     print()
            #     # print((ws.cell(row=j, column=i).value.strip()).split())
                # print(j, " ",(ws.cell(row=j, column=i).value.strip()))

# import requests
# surname = "Попов"
# initials = "ВВ"
# response = requests.get(
#     url=f"https://www.s-vfu.ru/stud/searchadddata.php?tablename=svfudbnew.forexcel&term={surname} {initials[0]}")
# data = response.json()
# # print(data)
# for d in data:
#     string = d.split()
#     if string[2].startswith(initials[1]):
#         print(d)
    


# from bs4 import BeautifulSoup


# def find_value_with_substring(html, substring):
#     soup = BeautifulSoup(html, 'html.parser')
#     select = soup.find('select')
#     if select:
#         options = select.find_all('option')
#         for option in options:
#             value = option.get('value')
#             if value and substring in value:
#                 return value
#     return None


# substring = "Б-М-21"
# html = 'Семестр 1<hr><select name="groupname"><optgroup label="Есть расписание"><option value="09.03.01|7618|ИМИ-Б-ИВТ-21-1|5954">(18.10 15:32) - ИМИ-Б-ИВТ-21-1(09.03.01-Технологии разработки программного обеспечения) -4 г. (20) </option><option value="01.03.01|7468|ИМИ-Б-М-21|5996">(24.10 12:09) - ИМИ-Б-М-21(01.03.01-Математика) -4 г. (10) </option><option value="02.03.02|7471|ИМИ-Б-ФИИТ-21|5998">(19.09 11:33) - ИМИ-Б-ФИИТ-21(02.03.02-Фундаментальная информатика и информационные технологии) -4 г. (21) </option><option value="09.03.01|7619|ИМИ-Б-ИВТ-21-2|5999">(19.09 11:17) - ИМИ-Б-ИВТ-21-2(09.03.01-Технологии разработки программного обеспечения) -4 г. (21) </option><option value="11.03.02|7467|ИМИ-Б-ИТСС-21|6003">(16.09 11:30) - ИМИ-Б-ИТСС-21(11.03.02-Инфокоммуникационные технологии и системы связи) -4 г. (18) </option><option value="44.03.01|7469|ИМИ-Б-МПО-21|6004">(15.09 12:51) - ИМИ-Б-МПО-21(44.03.01-Математика) -4 г. (13) </option><option value="44.03.05|7470|ИМИ-Б-ПОИМ-21|6005">(18.10 15:16) - ИМИ-Б-ПОИМ-21(44.03.05-Информатика и математика) -5 л. (13) </option><option value="09.03.03|7856|ИМИ-Б-ПИГМУ-21|6406">(27.09 14:13) - ИМИ-Б-ПИГМУ-21(09.03.03-Прикладная информатика в государственном и муниципальном управлении) -4 г. (18) </option><option value="09.03.03|7855|ИМИ-Б-ПИЭ-21|6407">(27.09 14:14) - ИМИ-Б-ПИЭ-21(09.03.03-Прикладная информатика в экономике) -4 г. (19) </option><option value="01.03.02|7623|ИМИ-Б-ПМИ-21|6724">(24.10 12:10) - ИМИ-Б-ПМИ-21(01.03.02-Прикладная математика и информатика) -4 г. (28) </option></select><button type="button" class="btn btn-primary" data-toggle="modal" data-target="#Modalrup" onclick="choicerup()">Подобрать РУП</button>'

# print(find_value_with_substring(html, substring))

# from openpyxl import load_workbook

# wb = load_workbook(
#     filename='flask\static\IMI rasp ochno 2 polug 2022-2023_28.02 (1).xlsx')
# sheets_names = wb.sheetnames

# groups = {
#     "Б-ИВТ-21-1": "09.03.01|7618|ИМИ-Б-ИВТ-21-1|5954",
#     "Б-М-21": "01.03.01|7468|ИМИ-Б-М-21|5996",
#     "Б-ФИИТ-21": "02.03.02|7471|ИМИ-Б-ФИИТ-21|5998",
#     "Б-ИВТ-21-2": "09.03.01|7619|ИМИ-Б-ИВТ-21-2|5999",
#     "Б-ИТСС-21": "11.03.02|7467|ИМИ-Б-ИТСС-21|6003",
#     "Б-МПО-21": "44.03.01|7469|ИМИ-Б-МПО-21|6004",
#     "Б-ПОИМ-21": "44.03.05|7470|ИМИ-Б-ПОИМ-21|6005",
#     "Б-ПИГМУ-21": "09.03.03|7856|ИМИ-Б-ПИГМУ-21|6406",
#     "Б-ПИЭ-21": "09.03.03|7855|ИМИ-Б-ПИЭ-21|6407",
#     "Б-ПМИ-21": "01.03.02|7623|ИМИ-Б-ПМИ-21|6724",
# }

# group_data = groups.get("Б-ПИЭ-21")

# print(group_data)

# # цикл по листам excel-файла
# # for sh in sheets_names:
# #     wb.active = sheets_names.index(sh)
# #     ws = wb.active
# #     schedule = {}
# #     weekday = ""
# #     course = ws.cell(row=2, column=1).value
# #     year_and_semestr = ws.cell(row=1, column=1).value
# #     if course is None and year_and_semestr is None:
# #         continue
# #     print(course, year_and_semestr)

# #     for row in ws.iter_rows():
# #         if row[0].value == "Суббота":
# #             max_row = row[0].row

# #     # цикл по всем группам
# #     for i in range(3, ws.max_column, 4):
# #         group_name = ws.cell(row=4, column=i).value
# #         if group_name != "**" and group_name != "*":
# #             # цикл по занятиям 1-ой группы
# #             for j in range(6, max_row + 1):
# #                 lesson = {}
# #                 if ws.cell(row=j, column=i).value is not None:
# #                     if ws.cell(row=j, column=1).value is not None:
# #                         weekday = ws.cell(row=j, column=1).value

# #                     lesson = {
# #                         "номер пары": j - 5,
# #                         "день недели": (weekday, ""),
# #                         "временной отрезок": (ws.cell(row=j, column=2).value, ""),
# #                         "название дисциплины": (ws.cell(row=j, column=3).value, ""),
# #                         "ФИО преподавателя": (ws.cell(row=j, column=4).value, ""),
# #                         "вид деятельности": (ws.cell(row=j, column=5).value, ""),
# #                         "номер аудитории": (ws.cell(row=j, column=6).value, ""),
# #                     }
# #                     schedule.setdefault(
# #                         group_name, []).append(lesson)
