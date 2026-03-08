from argparse import Namespace

from rich import print  # noqa: A004

from tiss_cli._store import TissData
from tiss_cli._utils import INFO_STYLE, ExitCode


def cmd_remove(args: Namespace) -> int:
    courses = TissData.read_from_data_dir()
    for course in courses.courses:
        if course.course_number == args.course:
            courses.courses.remove(course)
            print(f"{INFO_STYLE}removed {course}")
    courses.save_to_data_dir()
    return ExitCode.OK
