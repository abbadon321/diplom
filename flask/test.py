from openpyxl import load_workbook

wb = load_workbook(filename='flask\static\IMI rasp ochno 2 polug 2022-2023_28.02 (1).xlsx')
sheets_names = wb.sheetnames

# цикл по листам excel-файла
for sh in sheets_names:
    wb.active = sheets_names.index(sh)
    ws = wb.active
    schedule = {}
    weekday = ""
    course = ws.cell(row=2, column=1).value
    year_and_semestr = ws.cell(row=1, column=1).value
    if course is None and year_and_semestr is None:
        continue
    print(course, year_and_semestr)


    for row in ws.iter_rows():
        if row[0].value == "Суббота":
            max_row = row[0].row

    # цикл по всем группам
    for i in range(3, ws.max_column, 4):
        group_name = ws.cell(row=4, column=i).value
        if group_name != "**" and group_name != "*":
            # цикл по занятиям 1-ой группы
            for j in range(6, max_row + 1):
                lesson = {}
                if ws.cell(row=j, column=i).value is not None:
                    if ws.cell(row=j, column=1).value is not None:
                        weekday = ws.cell(row=j, column=1).value
                        
                    lesson = {
                        "номер пары": j - 5,
                        "день недели": (weekday, ""),
                        "временной отрезок": (ws.cell(row=j, column=2).value, ""),
                        "название дисциплины": (ws.cell(row=j, column=3).value, ""),
                        "ФИО преподавателя": (ws.cell(row=j, column=4).value, ""),
                        "вид деятельности": (ws.cell(row=j, column=5).value, ""),
                        "номер аудитории": (ws.cell(row=j, column=6).value, ""),
                    }
                    schedule.setdefault(
                        group_name, []).append(lesson)
