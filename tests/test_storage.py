import json
from pathlib import Path

import pytest

from student_records.models import Student
from student_records.records import StudentRecords
from student_records.storage import (
    StudentStorageError,
    load_records,
    save_records,
    student_from_data,
    student_to_data,
)


def test_student_to_data_converts_student_to_dictionary() -> None:
    student = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
        grades=[80, 90],
    )

    result = student_to_data(student)

    assert result == {
        "student_id": "S001",
        "name": "Htet Aung",
        "email": "htet@example.com",
        "grades": [80, 90],
    }


def test_student_from_data_creates_student() -> None:
    data = {
        "student_id": "S001",
        "name": "Htet Aung",
        "email": "htet@example.com",
        "grades": [80, 90],
    }

    student = student_from_data(data)

    assert student.student_id == "S001"
    assert student.name == "Htet Aung"
    assert student.email == "htet@example.com"
    assert student.grades == [80.0, 90.0]


def test_student_from_data_rejects_missing_required_field() -> None:
    data = {
        "student_id": "S001",
        "email": "htet@example.com",
        "grades": [80],
    }

    with pytest.raises(StudentStorageError, match="Missing or invalid text field"):
        student_from_data(data)


def test_student_from_data_rejects_invalid_grades() -> None:
    data = {
        "student_id": "S001",
        "name": "Htet Aung",
        "email": "htet@example.com",
        "grades": ["A"],
    }

    with pytest.raises(StudentStorageError, match="Each grade must be a number"):
        student_from_data(data)


def test_save_and_load_records_round_trip(tmp_path: Path) -> None:
    output_path = tmp_path / "students.json"

    records = StudentRecords()

    student_one = Student(
        student_id="S001",
        name="Htet Aung",
        email="htet@example.com",
        grades=[80, 90],
    )

    student_two = Student(
        student_id="S002",
        name="Alice Brown",
        email="alice@example.com",
        grades=[70],
    )

    records.add_student(student_one)
    records.add_student(student_two)

    save_records(records, output_path)
    loaded_records = load_records(output_path)

    assert loaded_records.student_count() == 2
    assert loaded_records.get_student("S001").name == "Htet Aung"
    assert loaded_records.get_student("S002").email == "alice@example.com"
    assert loaded_records.class_average() == 80.0


def test_load_records_rejects_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.json"

    with pytest.raises(StudentStorageError, match="Input file does not exist"):
        load_records(missing_file)


def test_load_records_rejects_invalid_json(tmp_path: Path) -> None:
    input_path = tmp_path / "students.json"
    input_path.write_text("{bad json", encoding="utf-8")

    with pytest.raises(StudentStorageError, match="Invalid JSON file"):
        load_records(input_path)


def test_load_records_rejects_missing_students_list(tmp_path: Path) -> None:
    input_path = tmp_path / "students.json"
    input_path.write_text(
        json.dumps({"records": []}),
        encoding="utf-8",
    )

    with pytest.raises(StudentStorageError, match="students list"):
        load_records(input_path)