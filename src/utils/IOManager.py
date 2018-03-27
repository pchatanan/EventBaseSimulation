import xlrd


def get_raw_data(file_path):
    workbook = xlrd.open_workbook(file_path)
    worksheet = workbook.sheet_by_index(0)

    first_row = []  # Header
    for col in range(worksheet.ncols):
        first_row.append(worksheet.cell_value(0, col))
    # transform the workbook to a list of dictionaries
    data = {}
    for col in range(len(first_row)):
        values = []
        for row in range(1, worksheet.nrows):
            values.append(worksheet.cell_value(row, col))
        data[first_row[col]] = values

    return data


def get_inter_arr_time(arr_time_list):
    inter_arr_time_list = []
    for i in range(1, len(arr_time_list)):
        inter_arr_time_list.append(arr_time_list[i] - arr_time_list[i - 1])
    return inter_arr_time_list
