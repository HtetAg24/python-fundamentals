import json
from pathlib import Path
from typing import Any

from student_records.models import Student
from student_records.records import StudentRecords


class StudentStorageError(ValueError):
    """Raised when student records storage operations are invalid."""


def student_to_data(student: Student) -> dict[str, object]:
    """Convert a Student object into JSON-serialisable data."""
    return {
        "student_id": student.student_id,
        "name": student.name,
        "email": student.email,
        "grades": student.grades,
    }


def _get_required_text(data: dict[str, Any], key: str) -> str:
    """Get and validate a required text field."""
    value = data.get(key)

    if not isinstance(value, str):
        raise StudentStorageError(f"Missing or invalid text field: {key}")

    return value


def _get_grades(data: dict[str, Any]) -> list[float]:
    """Get and validate grades from stored student data."""
    grades_value = data.get("grades", [])

    if not isinstance(grades_value, list):
        raise StudentStorageError("Grades must be stored as a list.")

    grades = []

    for grade in grades_value:
        if isinstance(grade, bool) or not isinstance(grade, int | float):
            raise StudentStorageError("Each grade must be a number.")

        grades.append(float(grade))

    return grades


def student_from_data(data: dict[str, Any]) -> Student:
    """Create a Student object from stored data."""
    student_id = _get_required_text(data, "student_id")
    name = _get_required_text(data, "name")
    email = _get_required_text(data, "email")
    grades = _get_grades(data)

    return Student(
        student_id=student_id,
        name=name,
        email=email,
        grades=grades,
    )


def save_records(records: StudentRecords, output_path: Path) -> None:
    """Save student records to a JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "students": [
            student_to_data(student)
            for student in records.list_students()
        ]
    }

    output_path.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8",
    )


def load_records(input_path: Path) -> StudentRecords:
    """Load student records from a JSON file."""
    if not input_path.exists():
        raise StudentStorageError(f"Input file does not exist: {input_path}")

    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))

    except json.JSONDecodeError as error:
        raise StudentStorageError("Invalid JSON file.") from error

    if not isinstance(data, dict):
        raise StudentStorageError("Stored records must be a JSON object.")

    students_data = data.get("students")

    if not isinstance(students_data, list):
        raise StudentStorageError("Stored records must contain a students list.")

    records = StudentRecords()

    for student_data in students_data:
        if not isinstance(student_data, dict):
            raise StudentStorageError("Each student record must be an object.")

        student = student_from_data(student_data)
        records.add_student(student)

    return records