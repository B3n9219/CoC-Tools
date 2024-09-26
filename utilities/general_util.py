def entire_column(column):
    return f"{column}:{column}"


def column_to_number(column_num):
    result = []
    while column_num > 0:
        column_num, remainder = divmod(column_num - 1, 26)
        result.append(chr(remainder + ord('A')))
    return ''.join(reversed(result))