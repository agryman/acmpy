from acmpy.so5cg import *
import os
from pathlib import Path
import pytest

# test database

# the SO5CG database base directory contains the level 1 directory dir1
test1_dir1_name: str = 'v2=2'
test1_dir1_label: int = 2

# the level 1 directory dir1 contains the level 2 directory dir2

test1_dir2_name: str = 'SO5CG_1_2_3'
test1_dir2_label: SO5Dir2Label = (1, 2, 3)

# the level 2 directory dir2 contains the data files file_1 and file_2
test1_file_1_name: str = 'SO5CG_1_2-1-2_3'
test1_file_1_label: SO5FileLabel = (1, 2, 1, 2, 3)

test1_file_2_name: str = 'SO5CG_1_2-1-4_3'
test1_file_2_label: SO5FileLabel = (1, 2, 1, 4, 3)

# the data file file_1 contains lines line_1, line_2, and line_3
test1_file_1_line_1: str = ' +1.000000e+00      1    1    2      2    1    2      3    1    0'
test1_file_1_data_1: SO5FileLine = (+1.000000e+00, ((1, 1, 2), (2, 1, 2), (3, 1, 0)))

test1_file_1_line_2: str = ' +8.451543e-01      1    1    2      2    1    2      3    1    3'
test1_file_1_data_2: SO5FileLine = (+8.451543e-01, ((1, 1, 2), (2, 1, 2), (3, 1, 3)))

test1_file_1_line_3: str = ' +7.237469e-01      1    1    2      2    1    2      3    1    4'
test1_file_1_data_3: SO5FileLine = (+7.237469e-01, ((1, 1, 2), (2, 1, 2), (3, 1, 4)))


class TestIsDirName:
    """Tests is_dir_name(name)."""

    def test_default(self):
        assert is_dir_name(default_base_name)


class TestParseDir1Name:
    """Tests parse_dir1_name(name)."""

    def test_valid(self):
        assert parse_dir1_name(test1_dir1_name) == test1_dir1_label
        assert parse_dir1_name('v2=7') == 7
        assert parse_dir1_name('v2=42') == 42

    def test_invalid(self):
        assert parse_dir1_name('v2=xxx') is None
        assert parse_dir1_name('xxx') is None

    def test_type_error(self):
        with pytest.raises(TypeError):
            parse_dir1_name(0)


class TestParseDir2Name:
    """Tests parse_dir2_name(name)."""

    def test_valid(self):
        assert parse_dir2_name(test1_dir2_name) == test1_dir2_label


class TestParseDatafileName:
    """Tests parse_datafile_name(name)."""

    def test_valid(self):
        assert parse_datafile_name(test1_file_1_name) == test1_file_1_label
        assert parse_datafile_name(test1_file_2_name) == test1_file_2_label


class TestParseLine:
    """Tests parse_line(line)."""

    def test_valid(self):
        assert parse_line(test1_file_1_line_1) == test1_file_1_data_1
        assert parse_line(test1_file_1_line_2) == test1_file_1_data_2
        assert parse_line(test1_file_1_line_3) == test1_file_1_data_3


class TestDatabase:
    """Creates a test fixture.

    TODO: turn this into a pytest test fixture.
    """

    def test_database(self, tmp_path: Path):
        # use tmp_path as the base directory of a test SO5CG database

        # create a level 1 directory
        test1_dir1: Path = tmp_path / test1_dir1_name
        test1_dir1.mkdir()

        # create a level 2 directory
        test1_dir2: Path = test1_dir1 / test1_dir2_name
        test1_dir2.mkdir()

        # create data file 1
        test1_file_1: Path = test1_dir2 / test1_file_1_name
        test1_file_1.touch()

        # create data file 2
        test1_file_2: Path = test1_dir2 / test1_file_2_name
        test1_file_2.touch()

        # write lines to data file 1
        lines = '\n'.join([test1_file_1_line_1, test1_file_1_line_2, test1_file_1_line_3]) + '\n'
        test1_file_1.write_text(lines)


if __name__ == "__main__":
    # TODO: convert this code into pytest test cases
    v2_dirs = [(entry.name, parse_dir1_name(entry.name)) for entry in os.scandir(default_base_name)
               if entry.is_dir() and parse_dir1_name(entry.name)]
    print(v2_dirs)

    print(parse_line(test1_file_1_line_1))
    print(parse_line(test1_file_1_line_2))
    print(parse_line(test1_file_1_line_3))

    base_dir = Path(default_base_name)
    test1_dir1 = base_dir / test1_dir1_name
    test1_dir2 = test1_dir1 / test1_dir2_name
    test1_file_1 = test1_dir2 / test1_file_1_name
    test1_file_2 = test1_dir2 / test1_file_2_name
    test1_paths = [test1_dir1, test1_dir2, test1_file_1, test1_file_2]

    print(test1_file_1, load_datafile(test1_file_1))
    print(test1_file_2, load_datafile(test1_file_2))

    print('Level 1 test:', test1_dir1.name, is_dir1_path(test1_dir1))
    print('Level 1 test:', test1_dir2.name, is_dir1_path(test1_dir2))
    print('Level 1 test:', test1_file_1.name, is_dir1_path(test1_file_1))
    print('Level 1 test:', test1_file_2.name, is_dir1_path(test1_file_2))

    print('Level 2 test:', test1_dir1.name, is_dir2_path(test1_dir1))
    print('Level 2 test:', test1_dir2.name, is_dir2_path(test1_dir2))
    print('Level 2 test:', test1_file_1.name, is_dir2_path(test1_file_1))
    print('Level 2 test:', test1_file_2.name, is_dir2_path(test1_file_2))

    print('Level 3 test:', test1_dir1.name, is_datafile_path(test1_dir1))
    print('Level 3 test:', test1_dir2.name, is_datafile_path(test1_dir2))
    print('Level 3 test:', test1_file_1.name, is_datafile_path(test1_file_1))
    print('Level 3 test:', test1_file_2.name, is_datafile_path(test1_file_2))

    print('Level 1 test:', [(path.name, is_dir1_path(path)) for path in test1_paths])
    print('Level 2 test:', [(path.name, is_dir2_path(path)) for path in test1_paths])
    print('Level 3 test:', [(path.name, is_datafile_path(path)) for path in test1_paths])

    print('Level 1 parse:', test1_dir1.name, parse_dir1_name(test1_dir1.name))
    print('Level 2 parse:', test1_dir2.name, parse_dir2_name(test1_dir2.name))
    print('Level 3 parse:', test1_file_1.name, parse_datafile_name(test1_file_1.name))
    print('Level 3 parse:', test1_file_2.name, parse_datafile_name(test1_file_2.name))

    print('Level 3 dict:', test1_file_1.name, datafile_dict(test1_file_1))
    print('Level 3 dict:', test1_file_2.name, datafile_dict(test1_file_2))

    print('Level 2 dict:', test1_dir2.name, dir2_dict(test1_dir2))

    print('Level 1 dict:', test1_dir1.name, len(dir1_dict(test1_dir1)))

    print('Level 0 dict:', base_dir.name, len(base_dict(base_dir)))
