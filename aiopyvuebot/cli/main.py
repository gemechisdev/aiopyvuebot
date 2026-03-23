"""Main CLI entry point for aiopyvuebot."""

import click

from aiopyvuebot import __version__
from aiopyvuebot.cli.commands.project import (
    init,
    install,
    dev,
    build,
    deploy,
    list_templates,
)
from aiopyvuebot.cli.commands.webhook import webhook


@click.group(invoke_without_command=True, context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--version", "-v", is_flag=True, help="Show version and exit.")
@click.pass_context
def cli(ctx: click.Context, version: bool) -> None:
    """
    aiopyvuebot – StarterKit CLI for Telegram Mini Apps.

    Scaffold a new project:

        aiopyvuebot init my-app

    Then install deps and start developing:

        cd my-app
        aiopyvuebot install
        aiopyvuebot dev
    """
    if version or ctx.invoked_subcommand is None:
        click.echo(f"aiopyvuebot {__version__}")


# Register commands
cli.add_command(init)
cli.add_command(install)
cli.add_command(dev)
cli.add_command(build)
cli.add_command(deploy)
cli.add_command(list_templates)
cli.add_command(webhook)


if __name__ == "__main__":
    cli()
