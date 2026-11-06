import math

MAX_MARKS = 100


def _to_float(value):
    """Convert a string to a finite float, or return None if invalid."""
    try:
        number = float(value.strip())
    except (ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def parse_applicant(text):
    """Parse 'category:marks' -> (Category, marks), or None if input is invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    category = parts[0].strip()
    marks = _to_float(parts[1])
    if not category or marks is None or not (0 <= marks <= MAX_MARKS):
        return None
    return category.title(), marks


def marks_average(marks_csv):
    """Average of comma-separated integer marks (0-100), or None if invalid."""
    if not isinstance(marks_csv, str):
        return None
    values = []
    for item in marks_csv.split(','):
        try:
            mark = int(item.strip())
        except (ValueError, OverflowError):
            return None
        if not (0 <= mark <= MAX_MARKS):
            return None
        values.append(mark)
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def payable_award(text):
    """Parse 'award|deduction' -> payable amount (>= 0), or None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    award = _to_float(parts[0])
    deduction = _to_float(parts[1])
    if award is None or deduction is None or award < 0 or deduction < 0:
        return None
    total = award * 1.18 - deduction
    if not math.isfinite(total):
        return None
    return round(max(total, 0), 2)


def _show(label, result):
    print(label, result if result is not None else "Invalid input")


def main():
    print("==== Running parse_applicant ====")
    user_input = input("Enter category:marks (e.g. merit:82): ")
    _show("Category and Marks:", parse_applicant(user_input))

    print("\n==== Running marks_average ====")
    user_input = input("Enter marks as CSV (e.g. 72,85,90): ")
    _show("Average Marks:", marks_average(user_input))

    print("\n==== Running payable_award ====")
    user_input = input("Enter award|deduction (e.g. 5000|500): ")
    _show("Payable Award:", payable_award(user_input))


if __name__ == "__main__":
    main()
