import json
from pathlib import Path

from student_records.cli import main


def create_example_file(file_path: Path) -> None:
    file_path.write_text(
        json.dumps(
            {
                "students": [
                    {
                        "student_id": "S001",
                        "name": "Htet Aung",
                        "email": "htet@example.com",
                        "grades": [80, 90],
                    },
                    {
                        "student_id": "S002",
                        "name": "Alice Brown",
                        "email": "alice@example.com",
                        "grades": [70],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )


def test_cli_lists_students(tmp_path: Path, capsys) -> None:
    file_path = tmp_path / "students.json"
    create_example_file(file_path)

    exit_code = main(["list", "--file", str(file_path)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "S001 | Htet Aung" in captured.out
    assert "S002 | Alice Brown" in captured.out


def test_cli_shows_student_by_id(tmp_path: Path, capsys) -> None:
    file_path = tmp_path / "students.json"
    create_example_file(file_path)

    exit_code = main(["show", "S001", "--file", str(file_path)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "S001 | Htet Aung" in captured.out
    assert "average: 85.00" in captured.out


def test_cli_adds_student(tmp_path: Path, capsys) -> None:
    file_path = tmp_path / "students.json"
    create_example_file(file_path)

    exit_code = main(
        [
            "add",
            "S003",
            "Charlie Green",
            "charlie@example.com",
            "--file",
            str(file_path),
        ]
    )

    captured = capsys.readouterr()
    saved_data = json.loads(file_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert "Added student: S003" in captured.out
    assert len(saved_data["students"]) == 3


def test_cli_adds_grade_to_student(tmp_path: Path, capsys) -> None:
    file_path = tmp_path / "students.json"
    create_example_file(file_path)

    exit_code = main(
        [
            "add-grade",
            "S001",
            "95",
            "--file",
            str(file_path),
        ]
    )

    captured = capsys.readouterr()
    saved_data = json.loads(file_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert "Added grade 95.0 to student: S001" in captured.out
    assert saved_data["students"][0]["grades"] == [80, 90, 95.0]


def test_cli_shows_class_average(tmp_path: Path, capsys) -> None:
    file_path = tmp_path / "students.json"
    create_example_file(file_path)

    exit_code = main(["class-average", "--file", str(file_path)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Class average: 80.00" in captured.out


def test_cli_returns_error_for_missing_student(tmp_path: Path, capsys) -> None:
    file_path = tmp_path / "students.json"
    create_example_file(file_path)

    exit_code = main(["show", "S999", "--file", str(file_path)])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: Student not found: S999" in captured.out


def test_cli_lists_empty_records_when_file_missing(tmp_path: Path, capsys) -> None:
    file_path = tmp_path / "missing.json"

    exit_code = main(["list", "--file", str(file_path)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "No students found." in captured.out