from openpyxl import Workbook
from openpyxl.styles import Font
import os


async def create_excel(user_list):
    wb = Workbook()
    ws = wb.active
    ws.append(
        (
            'ID пользователя',
            'Username пользователя',
            "Год рождения",
            "Рост",
            "Вес",
            "Курение",
            "Алкоголь",
        )
    )
    ft = Font(bold=True)
    for row in ws['A1:T1']:
        for cell in row:
            cell.font = ft

    for user in user_list:
        ws.append(
            (
                user['user_id'],
                user["username"],
                user["year"],
                user["height"],
                user["weight"],
                user["smoking"],
                user["drinking"],
            )
        )

    wb.save(f'{os.getcwd()}/user_list.xlsx')
