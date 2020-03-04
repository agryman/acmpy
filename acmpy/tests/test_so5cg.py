from acmpy.so5cg import *
import pytest

class TestIsDir:

    def test_default(self):
        assert is_dir(default_SO5CG_directory)


class TestParse_v2:

    def test_valid(self):
        assert parse_v2('v2=7') == 7
        assert parse_v2('v2=42') == 42

    def test_invalid(self):
        assert parse_v2('v2=xxx') is None
        assert parse_v2('xxx') is None

    def test_type_error(self):
        with pytest.raises(TypeError):
            parse_v2(0)

if __name__ == "__main__":
    v2_dirs = [(entry.name, parse_v2(entry.name)) for entry in os.scandir(default_SO5CG_directory) if entry.is_dir() and parse_v2(entry.name)]
    print(v2_dirs)

    test1_dir1_name = 'v2=2'
    test1_dir2_name = 'SO5CG_1_2_3'
    test1_file_1_name = 'SO5CG_1_2-1-2_3'
    test1_file_2_name = 'SO5CG_1_2-1-4_3'

    test_line_1 = ' +1.000000e+00      1    1    2      2    1    2      3    1    0'
    test_line_2 = ' +8.451543e-01      1    1    2      2    1    2      3    1    3'
    test_line_3 = ' +7.237469e-01      1    1    2      2    1    2      3    1    4'

    print(parse_line(test_line_1))
    print(parse_line(test_line_2))
    print(parse_line(test_line_3))

    base_dir = Path(default_SO5CG_directory)
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

    print('Level 2 test:', test1_dir1.name, is_level_2(test1_dir1))
    print('Level 2 test:', test1_dir2.name, is_level_2(test1_dir2))
    print('Level 2 test:', test1_file_1.name, is_level_2(test1_file_1))
    print('Level 2 test:', test1_file_2.name, is_level_2(test1_file_2))

    print('Level 3 test:', test1_dir1.name, is_datafile_path(test1_dir1))
    print('Level 3 test:', test1_dir2.name, is_datafile_path(test1_dir2))
    print('Level 3 test:', test1_file_1.name, is_datafile_path(test1_file_1))
    print('Level 3 test:', test1_file_2.name, is_datafile_path(test1_file_2))

    print('Level 1 test:', [(path.name, is_dir1_path(path)) for path in test1_paths])
    print('Level 2 test:', [(path.name, is_level_2(path)) for path in test1_paths])
    print('Level 3 test:', [(path.name, is_datafile_path(path)) for path in test1_paths])

    print('Level 1 parse:', test1_dir1.name, parse_dir1_name(test1_dir1.name))
    print('Level 2 parse:', test1_dir2.name, parse_level_2(test1_dir2.name))
    print('Level 3 parse:', test1_file_1.name, parse_datafile_name(test1_file_1.name))
    print('Level 3 parse:', test1_file_2.name, parse_datafile_name(test1_file_2.name))

    print('Level 3 dict:', test1_file_1.name, dict_level_3(test1_file_1))
    print('Level 3 dict:', test1_file_2.name, dict_level_3(test1_file_2))

    print('Level 2 dict:', test1_dir2.name, dict_level_2(test1_dir2))

    print('Level 1 dict:', test1_dir1.name, len(dict_level_1(test1_dir1)))

    print('Level 0 dict:', base_dir.name, len(dict_level_0(base_dir)))
