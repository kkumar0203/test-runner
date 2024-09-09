# Test Runner

A test runner in Python that mimics the behavior of pytest fixtures without using pytest. This framework allows you to define fixtures and tests in a similar manner to pytest. Primarily, you don't have to worry about setting up and
then safely closing/tearing down equipment after each test: through fixtures, you can define custom clean up logic or use context managers that will automatically setup and clean up resources after use.


## Features

- **Fixture Management**: Define and use fixtures with automatic setup and teardown.
- **Multiple Fixtures**: Create multiple fixtures in a test file. Each function can use multiple fixtures.
- **Nested Fixtures**: A fixture can also request other fixtures with support for deeply nested fixtures.
- **Isolation**: A new fixture is generated each time it is requested ensuring isolation between tests.
Automatic teardown of created fixtures in a test also ensure isolation. Teardown is conducted in reverse order, akin
to the fixtures in pytest, with the latest fixture being tordown first. This ensures safe cleanup, especially in the case
of nested fixtures.

- **Test Execution**: Run tests defined in Python files, with support for test files and directories.


## Installation

No installation is required. You only need to add the `tester.py` and `utils.py` scripts.

## Usage

### Define Fixtures and Tests

1. **Create a Test File**

    Define your fixtures and test functions in a Python file. Ensure that all functions in a test file
    have unique names. Start all test functions with the 'test_' prefix. If the parameter of a test
    function is a fixture, ensure that the parameter name matches the fixture function name.
    
    For example, create a file named `test_example.py`:

    ```python
    # test_example.py

    from tester import fixture

    @fixture
    def example_fixture():
        with open('example.txt', "w") as f:
            print('file opened')
            yield f
        print('file closed')

    def test_example(example_fixture):
        example_fixture.write("aaa")
        assert not example_fixture.closed

2. **Run Tests**

    You can run tests from the command line. Specify either a directory or a file containing test functions.
    Test files must start with the prefix 'test_' to be recognized.

    To run tests located in a directory (including all subdirectories), use the following command:

    ```sh
    python tester.py /path/to/test_directory
    ```

    To run tests located in a directory (including all subdirectories), use the following command:

    ```sh
    python tester.py /path/to/test_directory

