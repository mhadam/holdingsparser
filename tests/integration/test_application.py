from pathlib import Path

import pytest

from holdingsparser.application import get_save_path


def test_get_save_path_dir(tmp_path):
    term = "some_term"
    file_format = "dsv"

    result = get_save_path(tmp_path, term, file_format)

    assert result == tmp_path / Path(f"{term}_holdings.{file_format}")


def test_get_save_path_file(tmp_path):
    term = "some_term"
    file_format = "dsv"
    file_path = tmp_path / "some_file"

    result = get_save_path(file_path, term, file_format)

    assert result == file_path


def test_get_save_path_missing(tmp_path):
    term = "some_term"
    file_format = "dsv"
    file_path = tmp_path / "doesnt_exist" / "some_file"

    with pytest.raises(RuntimeError) as e:
        _ = get_save_path(file_path, term, file_format)

    assert str(e.value).endswith("is an invalid path")
