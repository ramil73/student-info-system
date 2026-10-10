"""Console entry point for the Student Information System.

Run from the project root:  python -m src.main
"""
from src.services.student_service import StudentService
from src.utils.config import load_config
from src.utils.exceptions import StudentError
from src.utils.logger import setup_logging

MENU = """
===== Student Information System =====
1. Add student
2. View all students
3. View one student
4. Update student
5. Delete student
6. Search students
7. Export to CSV
0. Exit
"""


def add(service):
    s = service.add_student(
        input("Student ID: "), input("Name: "), input("Age: "),
        input("Course: "), input("Email: "))
    print(f"Added: {s}")


def view_all(service):
    students = service.list_students()
    if not students:
        print("No students found.")
    for s in students:
        print(s)


def view_one(service):
    print(service.get_student(input("Student ID: ")))


def update(service):
    sid = input("Student ID to update: ")
    print("Leave a field blank to keep its current value.")
    s = service.update_student(
        sid, name=input("New name: "), age=input("New age: "),
        course=input("New course: "), email=input("New email: "))
    print(f"Updated: {s}")


def delete(service):
    sid = input("Student ID to delete: ")
    if input(f"Delete {sid}? (y/n): ").lower() == "y":
        service.delete_student(sid)
        print("Deleted.")
    else:
        print("Cancelled.")


def search(service):
    results = service.search(input("Search keyword: "))
    print(f"{len(results)} result(s):")
    for s in results:
        print(s)


def export(service, config):
    count = service.export_csv(config["export_file"])
    print(f"Exported {count} student(s) to {config['export_file']}")


def main():
    config = load_config()
    logger = setup_logging(config["log_file"], config["log_level"])
    logger.info("Application started.")
    try:
        service = StudentService(config["data_file"])
    except StudentError as exc:
        print(f"Startup error: {exc}")
        return

    actions = {"1": add, "2": view_all, "3": view_one, "4": update,
               "5": delete, "6": search, "7": lambda s: export(s, config)}

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            logger.info("Application exited.")
            print("Goodbye!")
            break
        action = actions.get(choice)
        if not action:
            print("Invalid option, please try again.")
            continue
        try:
            action(service)
        except StudentError as exc:  # expected, user-facing errors
            print(f"Error: {exc}")
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")
        except Exception:  # unexpected: log full traceback, keep app alive
            logger.exception("Unexpected error")
            print("Something went wrong. Details were written to the log file.")


if __name__ == "__main__":
    main()
