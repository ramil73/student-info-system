"""Student service: business logic and JSON persistence."""
import csv
import json
import logging
import os
import shutil
import tempfile
from datetime import datetime
from typing import List

from src.models.student import Student
from src.utils import validators
from src.utils.exceptions import (DuplicateStudentError, StorageError,
                                  StudentNotFoundError)

logger = logging.getLogger("sis.service")


class StudentService:
    """Handles CRUD, search and export for student records."""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.students = {}  # student_id -> Student
        self._load()

    # ---------- persistence ----------
    def _load(self) -> None:
        """Load students from JSON. A corrupted file is backed up, not lost."""
        if not os.path.exists(self.data_file):
            logger.info("Data file not found; starting empty.")
            self._save()
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
            self.students = {s["student_id"]: Student.from_dict(s) for s in raw}
            logger.info("Loaded %d students.", len(self.students))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            # Advanced error recovery: keep a backup of the bad file, start fresh
            backup = f"{self.data_file}.corrupt-{datetime.now():%Y%m%d%H%M%S}"
            shutil.copy(self.data_file, backup)
            logger.error("Data file corrupted (%s). Backup saved to %s", exc, backup)
            self.students = {}
            self._save()
        except OSError as exc:
            logger.exception("Cannot read data file.")
            raise StorageError(f"Cannot read data file: {exc}") from exc

    def _save(self) -> None:
        """Write atomically (temp file + replace) so a crash can't corrupt data."""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(self.data_file), suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump([s.to_dict() for s in self.students.values()], fh, indent=2)
            os.replace(tmp, self.data_file)
        except OSError as exc:
            logger.exception("Cannot write data file.")
            raise StorageError(f"Cannot write data file: {exc}") from exc

    # ---------- CRUD ----------
    def add_student(self, student_id, name, age, course, email) -> Student:
        student = Student(
            student_id=validators.validate_student_id(student_id),
            name=validators.validate_name(name),
            age=validators.validate_age(age),
            course=validators.validate_course(course),
            email=validators.validate_email(email),
        )
        if student.student_id in self.students:
            raise DuplicateStudentError(f"Student ID {student.student_id} already exists.")
        self.students[student.student_id] = student
        self._save()
        logger.info("Added student %s", student.student_id)
        return student

    def get_student(self, student_id: str) -> Student:
        try:
            return self.students[str(student_id).strip()]
        except KeyError:
            raise StudentNotFoundError(f"Student {student_id} not found.")

    def list_students(self) -> List[Student]:
        return sorted(self.students.values(), key=lambda s: s.student_id)

    def update_student(self, student_id, name=None, age=None, course=None, email=None) -> Student:
        """Update only the fields provided (None/blank = keep current value)."""
        student = self.get_student(student_id)
        if name:
            student.name = validators.validate_name(name)
        if age not in (None, ""):
            student.age = validators.validate_age(age)
        if course:
            student.course = validators.validate_course(course)
        if email:
            student.email = validators.validate_email(email)
        self._save()
        logger.info("Updated student %s", student.student_id)
        return student

    def delete_student(self, student_id: str) -> None:
        student = self.get_student(student_id)
        del self.students[student.student_id]
        self._save()
        logger.info("Deleted student %s", student.student_id)

    # ---------- bonus features ----------
    def search(self, keyword: str) -> List[Student]:
        """Case-insensitive search across ID, name, course and email."""
        kw = keyword.strip().lower()
        return [s for s in self.list_students()
                if kw in s.student_id.lower() or kw in s.name.lower()
                or kw in s.course.lower() or kw in s.email.lower()]

    def export_csv(self, path: str) -> int:
        """Export all students to CSV; returns number of rows written."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(
                    fh, fieldnames=["student_id", "name", "age", "course", "email"])
                writer.writeheader()
                for s in self.list_students():
                    writer.writerow(s.to_dict())
        except OSError as exc:
            logger.exception("Export failed.")
            raise StorageError(f"Export failed: {exc}") from exc
        logger.info("Exported %d students to %s", len(self.students), path)
        return len(self.students)
