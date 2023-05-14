from openpyxl import load_workbook

wb = load_workbook(
    filename='flask\static\IMI rasp ochno 2 polug 2022-2023_28.02 (1).xlsx')
sheets_names = wb.sheetnames

groups = {
    "Б-ИВТ-21-1": "09.03.01|7618|ИМИ-Б-ИВТ-21-1|5954",
    "Б-М-21": "01.03.01|7468|ИМИ-Б-М-21|5996",
    "Б-ФИИТ-21": "02.03.02|7471|ИМИ-Б-ФИИТ-21|5998",
    "Б-ИВТ-21-2": "09.03.01|7619|ИМИ-Б-ИВТ-21-2|5999",
    "Б-ИТСС-21": "11.03.02|7467|ИМИ-Б-ИТСС-21|6003",
    "Б-МПО-21": "44.03.01|7469|ИМИ-Б-МПО-21|6004",
    "Б-ПОИМ-21": "44.03.05|7470|ИМИ-Б-ПОИМ-21|6005",
    "Б-ПИГМУ-21": "09.03.03|7856|ИМИ-Б-ПИГМУ-21|6406",
    "Б-ПИЭ-21": "09.03.03|7855|ИМИ-Б-ПИЭ-21|6407",
    "Б-ПМИ-21": "01.03.02|7623|ИМИ-Б-ПМИ-21|6724",
}

group_data = groups.get("Б-ПИЭ-21")

print(group_data)

# цикл по листам excel-файла
# for sh in sheets_names:
#     wb.active = sheets_names.index(sh)
#     ws = wb.active
#     schedule = {}
#     weekday = ""
#     course = ws.cell(row=2, column=1).value
#     year_and_semestr = ws.cell(row=1, column=1).value
#     if course is None and year_and_semestr is None:
#         continue
#     print(course, year_and_semestr)

#     for row in ws.iter_rows():
#         if row[0].value == "Суббота":
#             max_row = row[0].row

#     # цикл по всем группам
#     for i in range(3, ws.max_column, 4):
#         group_name = ws.cell(row=4, column=i).value
#         if group_name != "**" and group_name != "*":
#             # цикл по занятиям 1-ой группы
#             for j in range(6, max_row + 1):
#                 lesson = {}
#                 if ws.cell(row=j, column=i).value is not None:
#                     if ws.cell(row=j, column=1).value is not None:
#                         weekday = ws.cell(row=j, column=1).value

#                     lesson = {
#                         "номер пары": j - 5,
#                         "день недели": (weekday, ""),
#                         "временной отрезок": (ws.cell(row=j, column=2).value, ""),
#                         "название дисциплины": (ws.cell(row=j, column=3).value, ""),
#                         "ФИО преподавателя": (ws.cell(row=j, column=4).value, ""),
#                         "вид деятельности": (ws.cell(row=j, column=5).value, ""),
#                         "номер аудитории": (ws.cell(row=j, column=6).value, ""),
#                     }
#                     schedule.setdefault(
#                         group_name, []).append(lesson)
