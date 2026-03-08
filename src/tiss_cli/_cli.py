"""A Commandline Interface for Tiss, the information system at TU Wien."""

from argparse import ArgumentParser, _SubParsersAction
from importlib.metadata import version

from tiss_cli import name
from tiss_cli._utils import ExitCode
from tiss_cli.cmd import cmd_add, cmd_list, cmd_list_courses, cmd_remove, cmd_sync

type SubParser = _SubParsersAction[ArgumentParser]


VERSION = version(name)


def build_parser() -> ArgumentParser:
    """Build the Argument Parser."""
    parser = ArgumentParser(
        prog="tiss-cli", description="Tiss CLI Tool", add_help=False
    )
    parser.add_argument("-h", "-help", action="help")
    parser.add_argument(
        "-v", "-version", action="version", version=f"%(prog)s {VERSION}"
    )
    subparsers: SubParser = parser.add_subparsers()
    register_add(subparsers)
    register_list(subparsers)
    register_remove(subparsers)
    register_sync(subparsers)
    register_list_courses(subparsers)
    return parser


def register_add(subparsers: SubParser) -> None:
    parser = subparsers.add_parser("add", help="Add a new entry", add_help=False)
    parser.add_argument("-h", "-help", action="help")
    parser.add_argument("course", help="The Course Number to add")
    parser.add_argument("-name", "-n", help="Set the name of the Course")
    parser.add_argument(
        "-credits", "-c", type=float, help="Set the credits of the Course"
    )
    parser.set_defaults(func=cmd_add)


def register_list(subparsers: SubParser) -> None:
    parser = subparsers.add_parser(
        "list", aliases=["ls"], help="List entries", add_help=False
    )
    parser.add_argument("-h", "-help", action="help")
    parser.set_defaults(func=cmd_list)


def register_list_courses(subparsers: SubParser) -> None:
    parser = subparsers.add_parser(
        "list-courses",
        aliases=["lc"],
        help="List all tracked courses",
        add_help=False,
    )
    parser.add_argument("-h", "-help", action="help")
    parser.set_defaults(func=cmd_list_courses)


def register_remove(subparsers: SubParser) -> None:
    parser = subparsers.add_parser(
        "remove", aliases=["rm"], help="Remove an entry", add_help=False
    )
    parser.add_argument("-h", "-help", action="help")
    parser.add_argument("course")
    parser.set_defaults(func=cmd_remove)


def register_sync(subparsers: SubParser) -> None:
    parser = subparsers.add_parser(
        "sync",
        help="Synchronize entries",
    )
    parser.set_defaults(func=cmd_sync)


def main_cli() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return ExitCode.OK
    return args.func(args)
