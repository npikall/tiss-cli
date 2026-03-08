from enum import IntEnum


class ExitCode(IntEnum):
    """Exit Codes for when sys.exit is called."""

    OK = 0
    ERROR = 1


INFO_STYLE: str = "[cyan]info[/cyan]: "
ERR_STYLE: str = "[red]error[/red]: "
