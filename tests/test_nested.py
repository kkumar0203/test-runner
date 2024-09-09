from tester import fixture


@fixture
def fix_1():
    yield [1]
    print("closed")

@fixture
def fix_2(fix_1):
    res = fix_1 + [2, 3]
    assert(res == [1, 2, 3])
    return res

@fixture
def fix_3(fix_2, fix_1):
    res = fix_2 + [4, 5] + fix_1
    assert(res == [1, 2, 3, 4, 5, 1])
    return res

@fixture
def fix_4():
    return ['lol']

def test_run(fix_3, fix_4):
    res = fix_3 + fix_4
    assert(res == [1, 2, 3, 4, 5, 1, 'lol'])
    print("passed")

def test_run_2(fix_4, fix_3, fix_1):
    res = fix_4 + fix_3 + fix_1
    print("res: ", res)
    assert(res == ['lol', 1, 2, 3, 4, 5, 1, 1])
