import asyncio
from argparse import Namespace
from datetime import date, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from defusedxml import ElementTree
from httpx import AsyncClient, HTTPStatusError, Response
from rich import print  # noqa: A004

from tiss_cli._store import CourseData, TissData
from tiss_cli._utils import ERR_STYLE, INFO_STYLE, ExitCode

if TYPE_CHECKING:
    from types import CoroutineType

BASE_URL = "https://tiss.tuwien.ac.at/api"
ROOT_PATH = Path(__file__).parent.parent.resolve()

REPLACEMENT_MAPPING: dict[str, str] = {
    " ": "_",
    "ä": "ae",
    "Ä": "Ae",
    "ö": "oe",
    "Ö": "Oe",
    "ü": "ue",
    "Ü": "Ue",
    "ß": "ss",
}


def get_exam_dates_endpoint(course_number: str) -> str:
    if "." in course_number:
        course_number = course_number.replace(".", "")
    return f"{BASE_URL}/course/{course_number}/examDates"


def sanitize_course_number(course_number: str) -> str:
    return course_number.replace(".", "")


def sanitize_course_name(course_name: str) -> str:
    for old, new in REPLACEMENT_MAPPING.items():
        course_name = course_name.replace(old, new)
    return course_name.casefold()


def parse_exam_dates_from_response(resp: Response) -> list[str | None]:
    root = ElementTree.fromstring(resp.content)
    return [elem.text for elem in root.findall(".//{*}examinationBegin")]


def convert_to_dates(optional_dates: list[str | None]) -> list[date]:
    return [
        datetime.fromisoformat(elem).date()
        for elem in optional_dates
        if elem is not None
    ]


async def fetch_exam(client: AsyncClient, url: str) -> Response:
    resp = await client.get(url, timeout=5)
    try:
        resp.raise_for_status()
    except HTTPStatusError:
        print(f"{ERR_STYLE}fetching {url}")
    return resp


async def fetch_exam_dates(
    client: AsyncClient,
    course: CourseData,
) -> CourseData:
    url: str = get_exam_dates_endpoint(course.course_number)
    resp: Response = await fetch_exam(client, url)
    maybe_dates: list[str | None] = parse_exam_dates_from_response(resp)
    exam_dates: list[date] = convert_to_dates(maybe_dates)
    course.exam_dates = exam_dates
    return course


async def fetch_all_exams(courses: list[CourseData]) -> list[CourseData]:
    async with AsyncClient() as client:
        tasks: list[CoroutineType[Any, Any, CourseData]] = [
            fetch_exam_dates(client, course) for course in courses
        ]
        return await asyncio.gather(*tasks)


def cmd_sync(args: Namespace) -> int:  # noqa: ARG001
    courses = TissData.read_from_data_dir()
    results = asyncio.run(fetch_all_exams(courses.courses))
    courses.courses = results
    courses.save_to_data_dir()
    print(f"{INFO_STYLE}synchronised")
    return ExitCode.OK
