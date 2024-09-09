from tester import fixture

def sneak_attack():
    return "sneak attack"

def test_no_fixture():
    print("no fixture test")

@fixture
def fix():
    with open("tests/txt_files/test_2_file_1.txt", "w") as f:
        print("file opened")
        yield f

    print("file closed")

def test_no_fixture_with_param(fix, sneak_attack=sneak_attack(), val=1):
    print(sneak_attack, val)
    fix.write("aaa")