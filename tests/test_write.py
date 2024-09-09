from tester import fixture

@fixture
def file_1():
    with open("tests/txt_files/file_1.txt", "w") as f:
        assert not f.closed
        print("file opened: 1")
        yield f

    assert f.closed
    print("file closed: 1")

@fixture
def file_1_a():
    with open("tests/txt_files/file_1.txt", "a") as f:
        assert not f.closed
        print("file opened: 1")
        yield f

    assert f.closed
    print("file closed: 1")

@fixture
def file_2():
    with open("tests/txt_files/file_2.txt", "w") as f:
        assert not f.closed
        print("file opened: 2")
        yield f

    assert f.closed
    print("file closed: 2")

@fixture
def file_3():
    with open("tests/txt_files/file_3.txt", "w") as f:
        assert not f.closed
        print("file opened: 3")
        yield f

    assert f.closed
    print("file closed: 3")

@fixture
def file_4():
    with open("tests/txt_files/file_4.txt", "w") as f:
        assert not f.closed
        print("file opened: 4")
        yield f

    assert f.closed
    print("file closed: 4")

@fixture
def value():
    return 1

def test_write_to_file_1_single_fixture(file_1):
    assert not file_1.closed
    file_1.write("test writing to file 1\n")
    print("test running...")
    assert not file_1.closed

def test_append_to_file_1_single_fixture(file_1_a):
    assert not file_1_a.closed
    file_1_a.write("test appending to file 1...again\n")
    print("test running...")
    assert not file_1_a.closed

def test_write_to__multiple_files_multiple_fixtures(file_2, file_3):
    assert not file_2.closed
    assert not file_3.closed
    file_2.write("test writing to file 2\n")
    file_3.write("test writing to file 3\n")
    print("test running...")
    assert not file_2.closed
    assert not file_3.closed

def test_non_yielding_fixture(value):
    print(value)

def test_combo_yeilding_and_non_yielding_fixtures(file_4, value):
    assert not file_4.closed
    file_4.write("test writing to file 4\n")
    print(value)
    assert not file_4.closed