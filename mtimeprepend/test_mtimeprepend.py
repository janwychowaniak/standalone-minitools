from mtimeprepend import epoch_to_yyyymmdd
from mtimeprepend import prepend
from mtimeprepend import update_dict


def test_epoch_to_yyyymmdd():

    assert epoch_to_yyyymmdd(1546702438) == '20190105'
    assert epoch_to_yyyymmdd(1548966952) == '20190131'


def test_prepend():

    assert prepend('name', 'prep') == 'prep-name'
    assert prepend('testname', '20190105') == '20190105-testname'


def test_update_dict():

    initial = {'mtimeprepend.py': '20190308',
               'mtimeprepend.pyc': '20190309',
               'cokolwiek': 'perp1234',
               'test_mtimeprepend.py': '12345678'}

    expected = {'mtimeprepend.py': '20190308-mtimeprepend.py',
                'mtimeprepend.pyc': '20190309-mtimeprepend.pyc',
                'cokolwiek': 'perp1234-cokolwiek',
                'test_mtimeprepend.py': '12345678-test_mtimeprepend.py'}

    assert update_dict(initial) == expected
