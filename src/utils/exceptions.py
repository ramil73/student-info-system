"""Custom exceptions so callers can handle specific failure cases."""


class StudentError(Exception):
    """Base class for all application errors."""


class ValidationError(StudentError):
    """Raised when user-supplied data is invalid."""


class DuplicateStudentError(StudentError):
    """Raised when adding a student whose ID already exists."""


class StudentNotFoundError(StudentError):
    """Raised when a student ID does not exist."""


class StorageError(StudentError):
    """Raised when reading or writing the data file fails."""
