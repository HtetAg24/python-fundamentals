import pytest

from student_records.models import Student, StudentValidationError


def test_student_can_be_created() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
    )

    assert student.student_id == "S001"
    assert student.name == "Htet Aung"
    assert student.email == "htet@example.com"
    assert student.grades == []


def test_student_cleans_text_fields() -> None:
    student = Student(
        student_id=" S001 ",
        name=" Htet Aung ",
        email=" HTET@EXAMPLE.COM ",
    )

    assert student.student_id == "S001"
    assert student.name == "Htet Aung"
    assert student.email == "htet@example.com"


def test_student_requires_student_id() -> None:
    with pytest.raises(StudentValidationError, match="Student ID is required"):
        Student(
            student_id="",
            name="Htet Aung",
            email="htet@example.com",
        )


def test_student_requires_name() -> None:
    with pytest.raises(StudentValidationError, match="Student name is required"):
        Student(
            student_id="S001",
            name="",
            email="htet@example.com",
        )


def test_student_rejects_invalid_email() -> None:
    with pytest.raises(StudentValidationError, match="Student email is invalid"):
        Student(
            student_id="S001",
            name="Htet Aung",
            email="invalid-email",
        )


def test_student_can_add_grade() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
    )

    student.add_grade(85)

    assert student.grades == [85.0]


def test_student_rejects_negative_grade() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
    )

    with pytest.raises(StudentValidationError, match="between 0 and 100"):
        student.add_grade(-10)


def test_student_rejects_grade_above_100() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
    )

    with pytest.raises(StudentValidationError, match="between 0 and 100"):
        student.add_grade(110)


def test_student_rejects_non_numeric_grade() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
    )

    with pytest.raises(StudentValidationError, match="Grade must be a number"):
        student.add_grade("A")  # type: ignore[arg-type]


def test_student_calculates_average_grade() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
        grades=[80, 90, 70],
    )

    assert student.average_grade() == 80.0


def test_student_average_is_none_when_no_grades() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
    )

    assert student.average_grade() is None


def test_student_passes_when_average_is_above_pass_mark() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
        grades=[60, 70],
    )

    assert student.has_passed() is True


def test_student_fails_when_average_is_below_pass_mark() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
        grades=[30, 35],
    )

    assert student.has_passed() is False


def test_student_to_dict_returns_summary() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
        grades=[80, 90],
    )

    assert student.to_dict() == {
        "student_id": "S001",
        "name": "Htet Aung",
        "email": "htet@example.com",
        "grades": [80, 90],
        "average_grade": 85.0,
        "has_passed": True,
    }