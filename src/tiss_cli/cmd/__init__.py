"""Commands for the application."""

from tiss_cli.cmd._add import cmd_add
from tiss_cli.cmd._list import cmd_list
from tiss_cli.cmd._remove import cmd_remove
from tiss_cli.cmd._sync import cmd_sync

__all__ = ["cmd_add", "cmd_list", "cmd_remove", "cmd_sync"]
