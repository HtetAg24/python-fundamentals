import pytest

from student_records.models import Student
from student_records.records import StudentRecords, StudentRecordsError


def make_student(
    student_id: str = "S001",
    name: str = "Htet Aung",
    email: str = "htet@example.com",
) -> Student:
    return Student(
        student_id=student_id,
        name=name,
        email=email,
    )


def test_student_records_can_add_and_get_student() -> None:
    records = StudentRecords()
    student = make_student()

    records.add_student(student)

    assert records.get_student("S001") == student
    assert records.student_count() == 1


def test_student_records_rejects_duplicate_student_id() -> None:
    records = StudentRecords()
    student = make_student()

    records.add_student(student)

    with pytest.raises(StudentRecordsError, match="Student already exists"):
        records.add_student(student)


def test_student_records_rejects_missing_student_id() -> None:
    records = StudentRecords()

    with pytest.raises(StudentRecordsError, match="Student not found"):
        records.get_student("S999")


def test_student_records_can_remove_student() -> None:
    records = StudentRecords()
    student = make_student()

    records.add_student(student)
    removed_student = records.remove_student("S001")

    assert removed_student == student
    assert records.student_count() == 0


def test_student_records_can_add_grade_to_existing_student() -> None:
    records = StudentRecords()
    student = make_student()

    records.add_student(student)
    records.add_grade("S001", 88)

    assert records.get_student("S001").grades == [88.0]


def test_student_records_lists_students_sorted_by_id() -> None:
    records = StudentRecords()

    records.add_student(make_student("S003", "Charlie", "charlie@example.com"))
    records.add_student(make_student("S001", "Alice", "alice@example.com"))
    records.add_student(make_student("S002", "Bob", "bob@example.com"))

    result = records.list_students()

    assert [student.student_id for student in result] == ["S001", "S002", "S003"]


def test_student_records_searches_by_name_case_insensitive() -> None:
    records = StudentRecords()

    records.add_student(make_student("S001", "Htet Aung", "htet@example.com"))
    records.add_student(make_student("S002", "Alice Brown", "alice@example.com"))

    result = records.search_by_name("htet")

    assert result == [records.get_student("S001")]


def test_student_records_finds_by_email_case_insensitive() -> None:
    records = StudentRecords()
    student = make_student("S001", "Htet Aung", "htet@example.com")

    records.add_student(student)

    result = records.find_by_email(" HTET@EXAMPLE.COM ")

    assert result == student


def test_student_records_rejects_unknown_email() -> None:
    records = StudentRecords()

    with pytest.raises(StudentRecordsError, match="Student email not found"):
        records.find_by_email("missing@example.com")


def test_student_records_calculates_class_average() -> None:
    records = StudentRecords()

    student_one = make_student("S001", "Alice", "alice@example.com")
    student_two = make_student("S002", "Bob", "bob@example.com")

    student_one.add_grade(80)
    student_one.add_grade(90)
    student_two.add_grade(70)

    records.add_student(student_one)
    records.add_student(student_two)

    assert records.class_average() == 80.0


def test_student_records_class_average_is_none_when_no_grades() -> None:
    records = StudentRecords()
    records.add_student(make_student())

    assert records.class_average() is None


def test_student_records_to_dict_returns_summary() -> None:
    records = StudentRecords()
    student = make_student()

    student.add_grade(80)
    student.add_grade(90)

    records.add_student(student)

    assert records.to_dict() == {
        "student_count": 1,
        "class_average": 85.0,
        "students": [
            {
                "student_id": "S001",
                "name": "Htet Aung",
                "email": "htet@example.com",
                "grades": [80.0, 90.0],
                "average_grade": 85.0,
                "has_passed": True,
            }
        ],
    }