from typing import TypedDict

import pytest

from tiss_cli._store import CourseData, TissData


class Case(TypedDict):
    number: str
    name: str | None
    want: str


test_data: list[Case] = [
    Case(number="123.123", name=None, want="123.123"),
    Case(number="123.123", name="FooBar", want="FooBar (123.123)"),
]


@pytest.mark.parametrize("case", test_data)
def test_CourseData_to_string_returns_correctly(case: Case):  # noqa: N802
    given = CourseData(course_number=case["number"], course_name=case["name"])
    got = given.to_string()
    assert got == case["want"]


def test_TissData_append_exam_works_correctly():  # noqa: N802
    course_1 = CourseData(course_number="123.123")
    course_2 = CourseData(course_number="321.321")

    got = TissData(courses=[course_1])
    got.append_exam(course_2)
    assert len(got.courses) == 2  # noqa: PLR2004
    assert got.courses == [course_1, course_2]


def test_TissData_contains_course_works_correctly():  # noqa: N802
    course_1 = CourseData(course_number="123.123")
    course_2 = CourseData(course_number="321.321")

    got = TissData(courses=[course_1])
    assert got.contains_course(course_1) is True
    assert got.contains_course(course_2) is False
