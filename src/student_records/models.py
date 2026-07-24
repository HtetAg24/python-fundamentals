from dataclasses import dataclass, field


class StudentValidationError(ValueError):
    """Raised when student data is invalid."""


@dataclass
class Student:
    """Represents a student record."""

    student_id: str
    name: str
    email: str
    grades: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate and clean student data after object creation."""
        self.student_id = self.student_id.strip()
        self.name = self.name.strip()
        self.email = self.email.strip().lower()

        self._validate_required_fields()
        self._validate_email()

        for grade in self.grades:
            self._validate_grade(grade)

    def _validate_required_fields(self) -> None:
        """Validate required text fields."""
        if not self.student_id:
            raise StudentValidationError("Student ID is required.")

        if not self.name:
            raise StudentValidationError("Student name is required.")

        if not self.email:
            raise StudentValidationError("Student email is required.")

    def _validate_email(self) -> None:
        """Validate student email address."""
        if "@" not in self.email or "." not in self.email:
            raise StudentValidationError("Student email is invalid.")

    @staticmethod
    def _validate_grade(grade: float) -> None:
        """Validate a grade value."""
        if isinstance(grade, bool) or not isinstance(grade, int | float):
            raise StudentValidationError("Grade must be a number.")

        if grade < 0 or grade > 100:
            raise StudentValidationError("Grade must be between 0 and 100.")

    def add_grade(self, grade: float) -> None:
        """Add a validated grade to the student."""
        self._validate_grade(grade)
        self.grades.append(float(grade))

    def average_grade(self) -> float | None:
        """Calculate the student's average grade."""
        if not self.grades:
            return None

        return round(sum(self.grades) / len(self.grades), 2)

    def has_passed(self, pass_mark: float = 40.0) -> bool:
        """Check whether the student has passed."""
        average = self.average_grade()

        if average is None:
            return False

        return average >= pass_mark

    def to_dict(self) -> dict[str, object]:
        """Convert the student record into a dictionary."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "grades": self.grades,
            "average_grade": self.average_grade(),
            "has_passed": self.has_passed(),
        }