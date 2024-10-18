def entire_column(column):
    return f"{column}:{column}"


def column_num_to_letter(column_num):
    result = []
    while column_num > 0:
        column_num, remainder = divmod(column_num - 1, 26)
        result.append(chr(remainder + ord('A')))
    return ''.join(reversed(result))


def strip_title(text):
    stripped_text = ""
    try:
        lines = text.splitlines()
        if len(lines) <= 1:
            return text.strip()
        return '\n'.join(line.strip() for line in lines)
    except:
        print(f"Unable to strip text: {text}")
        return None
