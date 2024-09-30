import click
from client_handler import create_client

@click.command()
@click.option(
    "-r", "--refresh-clients", is_flag=True, help="Flag to create a measurementlink client"
)
@click.option(
    "-s",
    "--sequence-directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True),
    help="Path to the directory where sequence files are stored",
)
def run_script(refresh_clients: bool, sequence_directory: str) -> None:
    """
    Python Custom Sequencer is a Command line tool which uses `Client generator` by integration and utilizes the clients to sequence measurements.
    """
    if refresh_clients:
        try:
            create_client(sequence_directory)
        except Exception as e:
            click.echo(f"An unexpected error occurred: {e}")
        return
    else:
        click.echo("No command specified. Use --help to look at options.")


if __name__ == "__main__":
    run_script()
