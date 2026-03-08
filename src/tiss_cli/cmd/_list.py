from argparse import Namespace
from datetime import date

from pydantic.dataclasses import dataclass
from rich.console import Console
from rich.table import Table

from tiss_cli._store import TissData
from tiss_cli._utils import ExitCode


@dataclass
class TableRow:
    number: str
    name: str | None
    date: date


def cmd_list(args: Namespace) -> int:  # noqa: ARG001
    data = TissData.read_from_data_dir()
    console = Console()
    table = Table(title="TU Exams")
    table.add_column("Date")
    table.add_column("Course")
    table.add_column("Name")
    unsorted_exams: set[tuple[date, str, str]] = set()
    for course in data.courses:
        if course.exam_dates is None:
            continue
        for exam in course.exam_dates:
            if course.course_name is None:
                course.course_name = ""
            unsorted_exams.add((exam, course.course_number, course.course_name))
    sorted_exams = sorted(unsorted_exams, key=lambda x: x[0])
    for row in sorted_exams:
        table.add_row(row[0].isoformat(), row[1], row[2])
    console.print(table)
    return ExitCode.OK
