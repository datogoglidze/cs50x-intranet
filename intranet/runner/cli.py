from typer import Typer

from intranet.runner.setup import setup

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "0.0.0.0", port: int = 5000) -> None:
    setup().run(host=host, port=port)
