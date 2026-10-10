"""Unit tests. Run from project root:  python -m unittest discover tests"""
import json
import os
import tempfile
import unittest

from src.services.student_service import StudentService
from src.utils.exceptions import (DuplicateStudentError, StudentNotFoundError,
                                  ValidationError)


class StudentServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "students.json")
        self.service = StudentService(self.path)
        self.service.add_student("S1", "Ana Cruz", 20, "BSCS", "ana@example.com")

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_and_get(self):
        self.assertEqual(self.service.get_student("S1").name, "Ana Cruz")

    def test_duplicate_id_rejected(self):
        with self.assertRaises(DuplicateStudentError):
            self.service.add_student("S1", "Bob Lim", 21, "BSIT", "bob@example.com")

    def test_update(self):
        self.service.update_student("S1", course="BSIT", age="22")
        s = self.service.get_student("S1")
        self.assertEqual((s.course, s.age), ("BSIT", 22))

    def test_delete(self):
        self.service.delete_student("S1")
        with self.assertRaises(StudentNotFoundError):
            self.service.get_student("S1")

    def test_validation(self):
        with self.assertRaises(ValidationError):
            self.service.add_student("S2", "X", 20, "BSCS", "bad-email")
        with self.assertRaises(ValidationError):
            self.service.add_student("S2", "Valid Name", "abc", "BSCS", "a@b.co")

    def test_persistence(self):
        reloaded = StudentService(self.path)
        self.assertEqual(len(reloaded.list_students()), 1)

    def test_search(self):
        self.assertEqual(len(self.service.search("bscs")), 1)
        self.assertEqual(len(self.service.search("zzz")), 0)

    def test_export_csv(self):
        out = os.path.join(self.tmp.name, "out.csv")
        self.assertEqual(self.service.export_csv(out), 1)
        self.assertTrue(os.path.exists(out))

    def test_corrupt_file_recovery(self):
        with open(self.path, "w") as fh:
            fh.write("{not valid json")
        recovered = StudentService(self.path)
        self.assertEqual(recovered.list_students(), [])
        backups = [f for f in os.listdir(self.tmp.name) if "corrupt" in f]
        self.assertEqual(len(backups), 1)
        with open(self.path) as fh:
            self.assertEqual(json.load(fh), [])


if __name__ == "__main__":
    unittest.main()
