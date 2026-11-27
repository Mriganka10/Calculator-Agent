#from calculator_agent import __main__


def calculate_percentage(marks_obtained, total_marks):
    if total_marks <= 0:
        raise ValueError("Total marks must be greater than zero.")

    if marks_obtained < 0 or marks_obtained > total_marks:
        raise ValueError("Marks must be between zero and total marks.")

    return (marks_obtained / total_marks) * 100

#This means:“Run these interactive instructions only when I run this file directly.”
if __name__ == "__main__":
    try:
        marks = float(input("Enter marks obtained: "))
        total = float(input("Enter total marks: "))


        result = calculate_percentage(marks, total)
        print("Your percentage is:", result)

    except ValueError as error:
        print("Invalid input:", error)