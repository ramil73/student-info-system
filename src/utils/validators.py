"""Input validation helpers (bonus feature: data validation)."""
import re

from src.utils.exceptions import ValidationError

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_student_id(student_id: str) -> str:
    student_id = str(student_id).strip()
    if not student_id:
        raise ValidationError("Student ID cannot be empty.")
    return student_id


def validate_name(name: str) -> str:
    name = str(name).strip()
    if len(name) < 2:
        raise ValidationError("Name must be at least 2 characters.")
    return name


def validate_age(age) -> int:
    try:
        age = int(age)
    except (TypeError, ValueError):
        raise ValidationError("Age must be a whole number.")
    if not 5 <= age <= 120:
        raise ValidationError("Age must be between 5 and 120.")
    return age


def validate_course(course: str) -> str:
    course = str(course).strip()
    if not course:
        raise ValidationError("Course cannot be empty.")
    return course


def validate_email(email: str) -> str:
    email = str(email).strip()
    if not EMAIL_PATTERN.match(email):
        raise ValidationError("Email address is not valid.")
    return email
