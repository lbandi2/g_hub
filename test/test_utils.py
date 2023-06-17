import pytest

from ..utils import read_csv, sanitize_path, file_from_path, check_process

def test_read_csv():
    test_data = [{'voltage': '4.186', 'percent': '100%'}, {'voltage': '4.156', 'percent': '99%'}]
    test_csv = read_csv('./test/sample.csv')
    assert test_data == test_csv

def test_sanitize_path_one_level():
    assert sanitize_path('/pepe.jpg') == '\\pepe.jpg'

def test_sanitize_path_two_levels():
    assert sanitize_path('/jose/pepe.jpg') == '\\jose\\pepe.jpg'

def test_file_from_path():
    assert file_from_path('/jose/pepe.jpg') == 'pepe.jpg'

def test_check_process_running():
    pass

def test_check_process_not_running():
    pass