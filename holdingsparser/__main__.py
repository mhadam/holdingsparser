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

from holdingsparser.application import search, get_output_rows

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
    if delimiter == ",":
        file_format = "csv"
    elif delimiter == r"\t":
        file_format = "tsv"
        delimiter = "\t"
    else:
        file_format = "dsv"
    if path:
        if not path.is_dir():
            save_path = path
        else:
            save_path = path / f"{term}_holdings.{file_format.lower()}"
    else:
        save_path = Path.cwd() / f"{term}_holdings.{file_format.lower()}"
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
