from tester import fixture

@fixture
def fix_1():
    print("opened: 1")
    yield 1
    print("closed: 1")

@fixture
def fix_2():
    print("opened: 2")
    yield 2
    print("closed: 2")

@fixture
def fix_3():
    print("opened: 3")
    yield 3
    print("closed: 3")

@fixture
def fix_4():
    print("opened: 4")
    yield 4
    print("closed: 4")

@fixture
def fix_5():
    print("opened: 5")
    yield 5
    print("closed: 5")

@fixture
def fix_6():
    print("opened: 6")
    yield 6
    print("closed: 6")

@fixture
def fix_7():
    print("opened: 7")
    yield 7
    print("closed: 7")

@fixture
def fix_8():
    print("opened: 8")
    yield 8
    print("closed: 8")

@fixture
def fix_9():
    print("opened: 9")
    yield 9
    print("closed: 9")

@fixture
def fix_10():
    print("opened: 10")
    yield 10
    print("closed: 10")

@fixture
def fix_11():
    print("opened: 11")
    yield 11
    print("closed: 11")

@fixture
def fix_12():
    print("opened: 12")
    yield 12
    print("closed: 12")

@fixture
def fix_13():
    print("opened: 13")
    yield 13
    print("closed: 13")

@fixture
def fix_14():
    print("opened: 14")
    yield 14
    print("closed: 14")

@fixture
def fix_15():
    print("opened: 15")
    yield 15
    print("closed: 15")

@fixture
def fix_16():
    print("opened: 16")
    yield 16
    print("closed: 16")

@fixture
def fix_17():
    print("opened: 17")
    yield 17
    print("closed: 17")

@fixture
def fix_18():
    print("opened: 18")
    yield 18
    print("closed: 18")

@fixture
def fix_19():
    print("opened: 19")
    yield 19
    print("closed: 19")

@fixture
def fix_20():
    print("opened: 20")
    yield 20
    print("closed: 20")

def test_run(fix_1, fix_2, fix_3, fix_4, fix_5, fix_6, fix_7, fix_8, fix_9, fix_10,
                      fix_11, fix_12, fix_13, fix_14, fix_15, fix_16, fix_17, fix_18, fix_19, fix_20):
    assert fix_1 == 1
    assert fix_2 == 2
    assert fix_3 == 3
    assert fix_4 == 4
    assert fix_5 == 5
    assert fix_6 == 6
    assert fix_7 == 7
    assert fix_8 == 8
    assert fix_9 == 9
    assert fix_10 == 10
    assert fix_11 == 11
    assert fix_12 == 12
    assert fix_13 == 13
    assert fix_14 == 14
    assert fix_15 == 15
    assert fix_16 == 16
    assert fix_17 == 17
    assert fix_18 == 18
    assert fix_19 == 19
    assert fix_20 == 20