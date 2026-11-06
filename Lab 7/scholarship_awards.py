def parse_applicant(text):
    category, marks = text.split(':')
    return category.strip().title(), float(marks)

def marks_average(marks_csv):
    values = [int(r) for r in marks_csv.split(',')]
    return sum(values) // len(values)

def payable_award(text):
    award, deduction = text.split('|')
    total = float(award) * 1.18 - float(deduction)
    return max(total, 0)

def main():
    print("==== Running parse_applicant ====")
    user_input = input("Enter category:marks (e.g. merit:82): ")
    result = parse_applicant(user_input)
    print("Category and Marks:", result)

    print("\n==== Running marks_average ====")
    user_input = input("Enter marks as CSV (e.g. 72,85,90): ")
    result = marks_average(user_input)
    print("Average Marks:", result)

    print("\n==== Running payable_award ====")
    user_input = input("Enter award|deduction (e.g. 5000|500): ")
    result = payable_award(user_input)
    print("Payable Award:", result)

if __name__ == "__main__":
    main()
