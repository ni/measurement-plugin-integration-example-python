"""Python sequencer package for sequencing measurement plug-ins using measurement plugin clients."""

import pathlib

import click

from python_sequencer._helpers import create_client


@click.command()
@click.argument(
    "directory_out",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True),
)
def run_script(directory_out: pathlib.Path) -> None:
    """The Python sequencer is a CLI tool that generates clients and a getting-started sequence using ni-measurement-plugin-client-generator.

    The `directory_out` argument is the path to the directory where sequence files are stored.
    """
    try:
        create_client(directory_out)
    except Exception as e:
        raise click.ClickException(f"An unexpected error occurred: {e}")
