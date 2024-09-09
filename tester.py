from inspect import Parameter, signature, isgenerator
from pathlib import Path
from utils import import_module_from_file
import argparse


def fixture(func):
    """
    Decorator to mark a function as a fixture.

    This decorator is used to indicate that a given function is a fixture, 
    similar to how pytest identifies fixtures.

    The 'fixture' decorator allows you to define functions that can set up 
    a context that other test functions can use. This is similar to the
    fixtures in pytest. When the tests are run, the fixtures are automatically
    recognized and handled.

    Args:
        func (function): The function to be marked as a fixture. 

    Returns:
        function: The original function wrapped and identified as a fixture.
    
    Example:
        @fixture
        def example_fixture():
            # setup code here
            yield value
            # teardown code here

        @fixture
        def example_fixture():
            with open("example.txt", "w") as f:
                yield f
    """

    func.is_fixture = True  # Fixture identifying flag.
    return func


class _Tester:
    """
    A test runner for executing all tests and fixtures within a single file or module.

    This class parses the provided test file, identifies fixture functions and test functions, 
    sets up the necessary fixtures and other parameters for each test, runs the tests,
    and cleans up/tears down any resources or running fixtures after the tests are executed.

    Attributes:
        _all_fixtures (dict): A dictionary mapping fixture function names to their respective functions.
        _running_fixtures (list): A list of currently running fixtures (fixtues that yield something)
        _tests (list): A list of test functions that need to be executed.
    """
    
    def __init__(self, test_file_path) -> None:
        """
        Initializes the test runner for the specified test file.

        Args:
            test_file_path (str): The path to the file containing test functions and fixtures.
        
        Raises:
            FileNotFoundError: If the specified test file does not exist.
        """

        self._all_fixtures = {}  # Fixture function name --> fixture function.
        self._running_fixtures = []  # List of all paused fixtures (i.e yield fixtures).
        self._tests = []  # List of all the test functions.

        # Update all_fixtures and tests by parsing through the given test_file_path.
        self._get_all_fixtures_and_tests(test_file_path)

    def _get_functions_names(self, test_file_path):
        """
        Parses the given file to retrieve the names of all functions defined in it.

        Args:
            test_file_path (str): The path to the file from which function names are extracted.
        
        Returns:
            list: A list of function names in the order they appear in the file.
        
        Raises:
            FileNotFoundError: If the file cannot be opened or read.
        """

        test_module = import_module_from_file(test_file_path)
        # Ensures that only one function name name is stored for each defined functions
        # because function names are assumed to be unique.
        func_names_set = set()
        func_names = []  # List of func_names in the order they appear

        # Open the python script with the tests for reading. Read line-by-line
        # and identify function names through common characteristics 
        # (i.e start with 'def', have '()').
        with open(test_file_path, 'r') as test_file:
            for line in test_file:
                strip = line.strip()
                if strip.startswith('def'):
                    # Strip white space, remove 'def ' and get string before first
                    # occurence of '('.
                    func_name = strip[len('def '):].split('(')[0]

                    # Ensure that function name is new and that a corresponding function exists.
                    if func_name not in func_names_set and hasattr(test_module, func_name):
                        func_names_set.add(func_name)
                        func_names.append(func_name)

        return func_names

    def _get_all_fixtures_and_tests(self, test_file_path):
        """
        Identifies and classifies functions in the given file as either fixtures or tests.

        Args:
            test_file_path (str): The path to the file containing functions.
        
        Raises:
            FileNotFoundError: If the file cannot be loaded or read.
        """

        test_module = import_module_from_file(test_file_path)
        func_names = self._get_functions_names(test_file_path)

        # Iterate through all functions to see which are fixtures
        # and which are tests.
        for func_name in func_names:
            func = getattr(test_module, func_name)  # Get actual func from name.
            if hasattr(func, 'is_fixture'):  # Func is a fixture.
                self._all_fixtures[func_name] = func
            elif func_name.startswith('test_'):  # Func is a test.
                self._tests.append(func)

    def _setup_fixtures(self, func):
        """
        Prepares the parameters in a function by running any requested fixtures 
        and returning their output.

        Args:
            func (function): The function that requires setup/output of fixtures and other parameters.
        
        Returns:
            dict:   If the function is a test function. Returns a dictionary that maps
                    parameter names to their corresponding values.
            object: If the function is a fixture function. Returns the output from running
                    the fixture function.

        Raises:
            TypeError:  If a required parameter is not a defined fixture and no
                        default value is given.
        """

        params = {}  # Dict of params in the func (param_name --> param_value)

        # Iterate through the function signature to get all params names
        # and any default values.
        for name, param in signature(func).parameters.items():
            if param.default is Parameter.empty:  # No default value.
                params[name] = None
            else:  # Has default value.
                params[name] = param.default

        # Recursive case: func has params. Recursively setup() each param.
        for name, value in params.items():
            # Only consider params that don't have a default value.
            # Cuch params reference fixture functions which must be ran for setup.
            if value is None:
                # If req param has no default val and is also not a fixture.
                if name not in self._all_fixtures:
                    msg = f"Missing required parameter. No fixture of name '{name}' " \
                            + "is defined and no default value is given."
                    raise TypeError(msg)
                # Param references a fixture function.
                fixture = self._all_fixtures[name]  # Using fixture name, get the corresponding func.
                # Recursively set up any params in the fixture function.
                fixture_output = self._setup_fixtures(fixture)
                # Store the output from running the fixture. To be used to run current func.
                params[name] = fixture_output
        
        # If the func is a test, setup is done. Return params so that the test can be executed.
        if func.__name__ not in self._all_fixtures:
            return params
        
        # Base case: func is a fixture. It either has no parameters or all or its
        # parameters have already been setup. In both cases, it is ready to be executed.
        output = func(**params)  # Unpack the keyword args and run the fixture function.

        if isgenerator(output):  # The fixture is a yield fixture.
            # Add the generator to the list of running fixtures that will be torndown after the test.
            self._running_fixtures.append(output) 
            # Iterate to a returnable obj in the generator. This is what the user expects to be
            # outputed from the fixture through yield.
            output = next(output)

        # Return the output of running the fixture to the caller test or fixture func.
        return output
    
    def _teardown_fixtures(self):
        """
        Cleans up any running fixtures by exhausting and closing
        yield-based fixtures.
        """

        # As per pytest fixture convention, teardown (execute code after the yield) of running
        # fixtures in reverse order. Most recent is torn down first.
        for yield_fixture in reversed(self._running_fixtures):
            try:
                for obj in yield_fixture:  # Exhaust the iterator because the test is already done.
                    next(yield_fixture)
            except StopIteration:  # Exception thrown when iterator is exhausted.
                pass
        self._running_fixtures = []  # all running fixtures have been cleaned up

    def run_tests(self):
        """
        Executes all test functions and handles their setup and teardown.

        Each test function is run with the appropriate fixtures set up beforehand. 
        After each test, any running fixtures are cleaned up.
        """

        # Iterate through and run all tests.
        for test in self._tests:
            params = self._setup_fixtures(test)  # Set up any necessary fixtures or default params.
            test(**params)  # Run the test with the setup params.
            self._teardown_fixtures()  # Teardown any running fixtures.


def main():
    """
    Executes tests in the specified file or directory.

    This function parses command-line arguments to determine the path to 
    a file or directory containing test files. It then locates Python files 
    that start with 'test_' and executes tests within them. If a directory 
    is specified, it searches recursively for test files. Tests with fixtures
    are automatically setup and torndown.

    Command-line Arguments:
        path_to_tests (str): The path to the test directory or file. If a 
                             directory is provided, it must exist and 
                             contain Python test files starting with 'test_'. 
                             If a file is provided, it must exist and be a 
                             Python file.

    Raises:
        FileNotFoundError: If the specified directory or file does not exist.

    Example Usage:
        To run tests in a directory:
            $ python tester.py /path/to/test_directory
        
        To run tests in a specific file:
            $ python tester.py /path/to/test_file.py
    """

    parser = argparse.ArgumentParser(prog='tester',
                                     description="Runs tests in files beginning with 'test_'")
    parser.add_argument('path_to_tests')  # Can be a directory or file.
    args = parser.parse_args()

    path = Path(args.path_to_tests)

    if path.is_dir():
        if not path.exists():
            raise FileNotFoundError(f"Test directory '{path}' does not exist.")
        path = path.resolve()  # Get the absolute path from the given path.
        for test_file in path.glob('**/*.py'):  # Recursively get all '.py' files.
            if str(test_file.name).startswith('test_'):  # Check that file is a test file.
                test_file_path = str(test_file)
                print(f"Running tests in file '{test_file_path}'")
                tester = _Tester(test_file_path)
                tester.run_tests()
                print('Passed\n')
    else:
        if not path.exists():
            raise FileNotFoundError(f"Test file '{path}' does not exist.")
        path = path.resolve()  # Get the absolute path from the given path.
        test_file_path = str(path)
        tester = _Tester(test_file_path)
        tester.run_tests()

if __name__ == '__main__':
    main()