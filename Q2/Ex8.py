import gspread
import numpy as np


def sheet_to_list(sheet):
    matrix = []
    mat_val = sheet.get_all_values()
    for mat_rows in mat_val:
        mat_row = []
        for num in mat_rows:
            mat_row.append(int(num))
        matrix.append(mat_row)
    return matrix


def login_to_google():
    account = gspread.service_account("researchalgorithms-dd8dddf9d7ac.json")
    spreadsheet = account.open("Ex8")
    A = spreadsheet.worksheet("A")
    B = spreadsheet.worksheet("B")
    sheet_list = [A, B]
    return sheet_list


def calc(first_matrix, second_matrix):
    np_matrix_a = np.array(first_matrix)
    np_matrix_b = np.array(second_matrix)
    ans = np.dot(np_matrix_a, np_matrix_b)
    return ans


def create_new_worksheet(ans):
    account = gspread.service_account("researchalgorithms-dd8dddf9d7ac.json")
    spreadsheet = account.open("Ex8")
    spreadsheet.add_worksheet(title="A_times_B", rows=ans.shape[0], cols=ans.shape[1])
    result_matrix = spreadsheet.worksheet("A_times_B")
    last_cell = chr(ord('A') + (ans.shape[1] - 1)) + str(ans.shape[0])
    sheet_to_write = "A1:" + last_cell
    result_matrix.update(sheet_to_write, ans.tolist())


if __name__ == '__main__':
    sheet_list = login_to_google()
    first_matrix = sheet_to_list(sheet_list[0])
    second_matrix = sheet_to_list(sheet_list[1])
    ans = calc(first_matrix, second_matrix)
    create_new_worksheet(ans)
