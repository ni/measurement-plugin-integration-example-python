import pathlib

import click

from ni_measurement_plugin_sequencer._helpers import create_client


@click.command()
@click.argument(
    "directory_out",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True),
)
def create_sequence(directory_out: pathlib.Path) -> None:
    """
    The Python sequencer is a CLI tool that uses the ni-measurement-plugin-client-generator to generate clients and creates a getting-started sequence.

    The `directory_out` argument is a mandatory path to the directory where sequence files are stored.
    """
    try:
        create_client(directory_out)
    except Exception as e:
        raise click.ClickException(f"An unexpected error occurred: {e}")
