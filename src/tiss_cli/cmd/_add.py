from argparse import Namespace

from rich import print  # noqa: A004

from tiss_cli._store import CourseData, TissData
from tiss_cli._utils import INFO_STYLE, ExitCode


def cmd_add(args: Namespace) -> int:
    course = CourseData(course_number=args.course, course_name=args.name)
    courses = TissData.read_from_data_dir()
    if not courses.contains_course(course):
        print(rf"{INFO_STYLE}adding {course.to_string()}")
        courses.append_exam(course)
        courses.save_to_data_dir()
        return ExitCode.OK
    print(rf"{INFO_STYLE}{course.to_string()} is already added")
    return ExitCode.OK
