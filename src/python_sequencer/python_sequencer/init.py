import pathlib
import click

from python_sequencer._client_handler import create_client


@click.command()
@click.argument(
    "directory_out",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True),
)
def run_script(directory_out: pathlib.Path) -> None:
    """
    Python Custom Sequencer is a Command line tool which uses `Client generator` by integration and utilizes the clients to sequence measurements.
    
    The `directory_out` argument is a mandatory path to the directory where sequence files are stored.
    """
    try:
        create_client(directory_out)
    except Exception as e:
        raise click.ClickException(f"An unexpected error occurred: {e}")
