from datetime import date
from pathlib import Path

from platformdirs import PlatformDirs
from pydantic import BaseModel


class CourseData(BaseModel):
    course_number: str
    course_name: str | None = None
    exam_dates: list[date] | None = None

    def to_string(self) -> str:
        if self.course_name is not None:
            return f"{self.course_name} ({self.course_number})"
        return f"{self.course_number}"


class TissData(BaseModel):
    courses: list[CourseData]

    def append_exam(self, exam: CourseData) -> None:
        if not self.contains_course(exam):
            self.courses.append(exam)

    def contains_course(self, other: CourseData) -> bool:
        return any(e.course_number == other.course_number for e in self.courses)

    def save_to_data_dir(self) -> None:
        storage: Path = get_storage_filepath()
        storage.touch()
        storage.write_text(self.model_dump_json(indent=2))

    @staticmethod
    def read_from_data_dir() -> "TissData":
        storage: Path = get_storage_filepath()
        if not storage.exists():
            return TissData(courses=[])
        return TissData.model_validate_json(storage.read_bytes())


def get_platformdirs() -> PlatformDirs:
    return PlatformDirs(appname="tiss-cli")


def get_storage_filepath() -> Path:
    dirs = get_platformdirs()
    dirs.user_data_path.mkdir(exist_ok=True, parents=True)
    return dirs.user_data_path / "storage.json"
