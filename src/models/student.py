"""Student model: a plain data container with (de)serialization helpers."""
from dataclasses import dataclass, asdict


@dataclass
class Student:
    """Represents a single student record."""
    student_id: str
    name: str
    age: int
    course: str
    email: str

    def to_dict(self) -> dict:
        """Convert the student to a JSON-serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """Build a Student from a dictionary (e.g. loaded from JSON)."""
        return cls(
            student_id=str(data["student_id"]),
            name=data["name"],
            age=int(data["age"]),
            course=data["course"],
            email=data["email"],
        )

    def __str__(self) -> str:
        return (f"[{self.student_id}] {self.name} | Age: {self.age} | "
                f"Course: {self.course} | Email: {self.email}")
