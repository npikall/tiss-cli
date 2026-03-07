"""tiss-cli: A Package to..."""

from importlib.metadata import version

__version__ = version(__name__)

name = "tiss_cli"


def greet() -> str:
    """Greet the User."""
    return "Hello from tiss-cli"
