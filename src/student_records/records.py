from dataclasses import dataclass, field

from student_records.models import Student


class StudentRecordsError(ValueError):
    """Raised when student records operations are invalid."""


@dataclass
class StudentRecords:
    """Manages a collection of student records."""

    students: dict[str, Student] = field(default_factory=dict)

    def add_student(self, student: Student) -> None:
        """Add a student to the records."""
        if student.student_id in self.students:
            raise StudentRecordsError(
                f"Student already exists: {student.student_id}"
            )

        self.students[student.student_id] = student

    def get_student(self, student_id: str) -> Student:
        """Get a student by student ID."""
        clean_student_id = student_id.strip()

        if clean_student_id not in self.students:
            raise StudentRecordsError(f"Student not found: {clean_student_id}")

        return self.students[clean_student_id]

    def remove_student(self, student_id: str) -> Student:
        """Remove and return a student by student ID."""
        student = self.get_student(student_id)
        del self.students[student.student_id]

        return student

    def add_grade(self, student_id: str, grade: float) -> None:
        """Add a grade to an existing student."""
        student = self.get_student(student_id)
        student.add_grade(grade)

    def list_students(self) -> list[Student]:
        """Return all students sorted by student ID."""
        return [
            self.students[student_id]
            for student_id in sorted(self.students)
        ]

    def search_by_name(self, query: str) -> list[Student]:
        """Search students by name using a case-insensitive partial match."""
        clean_query = query.strip().lower()

        return [
            student
            for student in self.list_students()
            if clean_query in student.name.lower()
        ]

    def find_by_email(self, email: str) -> Student:
        """Find a student by email address."""
        clean_email = email.strip().lower()

        for student in self.students.values():
            if student.email == clean_email:
                return student

        raise StudentRecordsError(f"Student email not found: {clean_email}")

    def student_count(self) -> int:
        """Return the number of students in the records."""
        return len(self.students)

    def class_average(self) -> float | None:
        """Calculate the average grade across all stored grades."""
        all_grades = [
            grade
            for student in self.students.values()
            for grade in student.grades
        ]

        if not all_grades:
            return None

        return round(sum(all_grades) / len(all_grades), 2)

    def to_dict(self) -> dict[str, object]:
        """Convert the records into a dictionary summary."""
        return {
            "student_count": self.student_count(),
            "class_average": self.class_average(),
            "students": [
                student.to_dict()
                for student in self.list_students()
            ],
        }