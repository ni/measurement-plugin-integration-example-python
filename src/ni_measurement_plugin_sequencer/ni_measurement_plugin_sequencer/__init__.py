"""NI Measurement Plug-In Sequencer for Python."""

import pathlib

import click

from ni_measurement_plugin_sequencer._helpers import create_client


@click.command()
@click.argument(
    "directory_out",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True),
)
def create_sequence(directory_out: pathlib.Path) -> None:
    """Creates a sequence by generating clients using the ni-measurement-plugin-client-generator.

    Args:
        directory_out: Path to the directory where sequence files are stored.

    Raises:
        click.ClickException: An unexpected error occurred during client creation.
    """
    try:
        create_client(directory_out)
    except Exception as e:
        raise click.ClickException(f"An unexpected error occurred: {e}")
