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


class Format(str, Enum):
    CSV = "csv"
    TSV = "tsv"


@app.command()  # only entrypoint for Typer now
def main_command(
    term: str = typer.Argument(..., help="Name, ticker or CIK"),
    verbose: int = typer.Option(0, "--verbose", "-v", count=True),
    format_: Format = typer.Option(Format.CSV, "--format", "-f", case_sensitive=False),
    path: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Path of directory to write output file"
    ),
):
    if verbose > 0:
        configure_logging(verbose)
    logger.debug(f"{verbose=}")
    if format_ == Format.CSV:
        delimiter = ","
    elif format_ == Format.TSV:
        delimiter = "\t"
    else:
        raise RuntimeError(f"{format_} is not a valid delimiter")
    if path:
        if not path.exists():
            raise RuntimeError(f"{path} does not exist")
        if not path.is_dir():
            raise RuntimeError(f"{path} is not a directory")
        save_path = path
    else:
        save_path = Path.cwd()
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
        with open(
            save_path / f"{term}_holdings.{format_.value.lower()}", "w"
        ) as dsvfile:
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
