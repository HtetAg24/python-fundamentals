import argparse
from argparse import Namespace
from pathlib import Path

from student_records.models import Student, StudentValidationError
from student_records.records import StudentRecords, StudentRecordsError
from student_records.storage import (
    StudentStorageError,
    load_records,
    save_records,
)


DEFAULT_DATA_FILE = Path("examples/students.json")


def load_records_or_empty(file_path: Path) -> StudentRecords:
    """Load records from a JSON file, or return empty records if the file does not exist."""
    if not file_path.exists():
        return StudentRecords()

    return load_records(file_path)


def format_average(average: float | None) -> str:
    """Format an average grade for display."""
    if average is None:
        return "N/A"

    return f"{average:.2f}"


def format_grades(grades: list[float]) -> str:
    """Format grades for display."""
    if not grades:
        return "none"

    return ", ".join(str(grade) for grade in grades)


def format_student(student: Student) -> str:
    """Format one student for terminal output."""
    passed_text = "yes" if student.has_passed() else "no"

    return (
        f"{student.student_id} | "
        f"{student.name} | "
        f"{student.email} | "
        f"grades: {format_grades(student.grades)} | "
        f"average: {format_average(student.average_grade())} | "
        f"passed: {passed_text}"
    )


def handle_list(args: Namespace) -> int:
    """Handle the list command."""
    records = load_records_or_empty(Path(args.file))
    students = records.list_students()

    if not students:
        print("No students found.")
        return 0

    for student in students:
        print(format_student(student))

    return 0


def handle_show(args: Namespace) -> int:
    """Handle the show command."""
    records = load_records_or_empty(Path(args.file))
    student = records.get_student(args.student_id)

    print(format_student(student))

    return 0


def handle_add(args: Namespace) -> int:
    """Handle the add command."""
    file_path = Path(args.file)
    records = load_records_or_empty(file_path)

    student = Student(
        student_id=args.student_id,
        name=args.name,
        email=args.email,
    )

    records.add_student(student)
    save_records(records, file_path)

    print(f"Added student: {student.student_id}")

    return 0


def handle_add_grade(args: Namespace) -> int:
    """Handle the add-grade command."""
    file_path = Path(args.file)
    records = load_records_or_empty(file_path)

    records.add_grade(args.student_id, args.grade)
    save_records(records, file_path)

    print(f"Added grade {args.grade} to student: {args.student_id}")

    return 0


def handle_class_average(args: Namespace) -> int:
    """Handle the class-average command."""
    records = load_records_or_empty(Path(args.file))
    average = records.class_average()

    print(f"Class average: {format_average(average)}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Manage student records from the command line."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--file",
        default=str(DEFAULT_DATA_FILE),
        help="Path to the student records JSON file.",
    )

    subparsers.add_parser(
        "list",
        parents=[common_parser],
        help="List all students.",
    )

    show_parser = subparsers.add_parser(
        "show",
        parents=[common_parser],
        help="Show one student by ID.",
    )
    show_parser.add_argument("student_id")

    add_parser = subparsers.add_parser(
        "add",
        parents=[common_parser],
        help="Add a new student.",
    )
    add_parser.add_argument("student_id")
    add_parser.add_argument("name")
    add_parser.add_argument("email")

    add_grade_parser = subparsers.add_parser(
        "add-grade",
        parents=[common_parser],
        help="Add a grade to an existing student.",
    )
    add_grade_parser.add_argument("student_id")
    add_grade_parser.add_argument("grade", type=float)

    subparsers.add_parser(
        "class-average",
        parents=[common_parser],
        help="Show the class average.",
    )

    return parser


def run_command(args: Namespace) -> int:
    """Run the selected CLI command."""
    if args.command == "list":
        return handle_list(args)

    if args.command == "show":
        return handle_show(args)

    if args.command == "add":
        return handle_add(args)

    if args.command == "add-grade":
        return handle_add_grade(args)

    if args.command == "class-average":
        return handle_class_average(args)

    raise ValueError(f"Unknown command: {args.command}")


def main(argv: list[str] | None = None) -> int:
    """Run the Student Records CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return run_command(args)

    except (
        StudentValidationError,
        StudentRecordsError,
        StudentStorageError,
        ValueError,
    ) as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())