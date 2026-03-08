"""tiss-cli: A Package to..."""

from importlib.metadata import version

__version__ = version(__name__)

name = "tiss_cli"

from tiss_cli._cli import main_cli

__all__ = ["main_cli"]
