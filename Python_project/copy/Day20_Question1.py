# 1. Sort Students by Grade (Descending)
def sort_students_by_grade(students):
    # Sorts a list of (name, grade) tuples by grade in descending order.
    return sorted(students, key=lambda x: x[1], reverse=True)

# Example usage:
if __name__ == "__main__":
    # 1. Sort Students by Grade
    students1 = [("Ram", 85), ("Bhuvi", 92), ("Chetan", 78)]
    print(sort_students_by_grade(students1)) 

    students2 = [("Jatin", 88), ("Sarah", 95), ("Mona", 82), ("Aadi", 95)]
    print(sort_students_by_grade(students2)) 