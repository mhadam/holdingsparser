import logging
import sys

import typer
import requests_random_user_agent  # NOTE: this enables random user agents

from holdingsparser.application import search

logger = logging.getLogger(__name__)


app = typer.Typer()


def configure_logging(verbose: int):
    level = logging.ERROR - (verbose - 1) * 10
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=level
    )


@app.command()  # only entrypoint for Typer now
def main_command(
    term: str = typer.Argument(..., help="Name, ticker or CIK"),
    verbose: int = typer.Option(0, "--verbose", "-v", count=True),
):
    if verbose > 0:
        configure_logging(verbose)
    logger.debug(f"{verbose=}")
    try:
        search(term)
    except RuntimeError as e:
        if verbose:
            logging.exception(str(e))
        else:
            print(str(e))
        sys.exit(2)


def main():
    app()


if __name__ == "__main__":
    main()
