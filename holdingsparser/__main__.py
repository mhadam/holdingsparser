import csv
import logging
import shutil
import sys
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Optional

import typer
import requests_random_user_agent  # NOTE: this enables random user agents

from holdingsparser.application import (
    search,
    get_output_rows,
    get_save_path,
    get_file_format,
)

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
    delimiter: str = typer.Option(
        ",", "--delimiter", "-d", help="Delimiter used between values"
    ),
    path: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Path of directory to write output file"
    ),
):
    if verbose > 0:
        configure_logging(verbose)
    logger.debug(f"{verbose=}")

    file_format = get_file_format(delimiter)
    if delimiter == r"\t":
        delimiter = "\t"
    save_path = get_save_path(path, term, file_format)

    try:
        holding_stream = search(term)
        output_rows_stream = get_output_rows(holding_stream)
        try:
            column_names = next(output_rows_stream)
        except StopIteration:
            raise RuntimeError("failed to get file output header")
        result = StringIO()
        w = csv.DictWriter(result, column_names, delimiter=delimiter)
        w.writeheader()
        for row in output_rows_stream:
            w.writerow(row)
        print(result.getvalue(), end="")
        with open(save_path, "w") as dsvfile:
            result.seek(0)
            shutil.copyfileobj(result, dsvfile)
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
