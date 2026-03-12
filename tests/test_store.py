import pytest  # noqa: F401

from tiss_cli._store import CourseData


def test_CourseData_to_string_returns_correctly():  # noqa: N802
    given = CourseData(course_number="123.123")
    got = given.to_string()
    want = "123.123"
    assert got == want
