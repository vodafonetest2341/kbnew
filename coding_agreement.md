# Coding agreement

## Purpose of this document

This document sets a baseline to ensure code quality during a project. It provides guidelines on Python coding best practices.
You will also find insights on responsibilities expected from a developer / data scientist before opening a Pull Request, and from a reviewer to ensure a good and constructive review.

## Code reviews

[Code reviews](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/inclusion-in-code-review/) are an important part of our job as developers. They help ensure the quality of our work, share it with others, and grow together as a team while improving code quality and sharing understanding. When a review is conducted, [be open to feedback](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/author-guidance/#be-open-to-receive-feedback) and [Be inclusive, and foster a positive code review culture](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/#foster-a-positive-code-review-culture).

## Tooling used

- Code linter:
  - [Black](https://code.visualstudio.com/docs/python/formatting)
  - [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)
  - [Behave]()
  - [Bandit](https://github.com/PyCQA/bandit)
  - [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)

## Coding guidelines

This coding agreement provides some guidelines for Python, but they can be adapted to any other programming language.

The guidelines in this section need to be followed by developers / data scientists. Reviewers will also need to validate these guidelines during PR review. The comments in brackets next to the section title refer to production-ready code. Experimental or exploratory code does not need to strictly follow these guidelines. However, it is recommended that most of the rules are followed, because then it will be much easier to convert experimental code into production-ready code when needed.

### Code Layout [MUST]

- `import`: first standard libraries, then third party and finally local libraries. All groups alphabetically sorted.
- `blank lines`: two blank lines surrounding classes and top-level functions. Methods inside functions are surrounded by a single line.
- `indentation`: use 4 spaces (most IDEs will convert tab into 4 spaces by default).
- `line length`: maximum 88 chars.

```python
# Standard libs
import std_lib_1
import std_lib_2

# Third party libs
import third_party_lib_1
import third_party_lib_2

# Local lib
from local_lib import class_1, function_1


# After two blank lines
def top_level_function(args: int) -> str:
    # Body
```

### String quotes, whitespaces [MUST]

- `whitespace`: avoid extra white spaces, use single white spaces around both sides of an operator, one after comma and none inside opening or closing parenthesis.
- `quotes`: use double quotes. Single quotes can be used for strings if for instance you need to encapsulate json (which contains double quotes). But the rule is double quotes everywhere else.

```python
x = "Hello world"
y = 15

print(x)
```

### Naming convention [MUST]

- `language, spelling`: 
  - Class names, function names, and variable names are written in English. Use meaningful and grammatically correct names.
  - Use verbs to name functions and methods (they are actions), and names to name variables and classes (they are things).
- `class name`: name should start with an __uppercase__ and follow the camelCase convention if it has more than two words.
- `function name`:
  - lowercase, words separated by an underscore.
  - add `self` argument at first position if the method is a class's method.
  - if the function's name clashes with a reserved word, append underscore.
  - use 1 underscores at the beginning for private class's methods.
  - use 1 underscore at the beginning of a private field.
  - specify the type of your input parameters
  - always provide a return type (use 'None' if 'void').
- `variable name`: lowercase, words separated by an underscore.

```python
class CatalogInformation:
    def __init__(self, name: str) -> None:
        # Body constructor

    def get_metadata_count(self) -> int:
        # Body method
        return 1

    def _check_internal_property(self) -> bool:
        # Body private method
        return True
```

### Comments / documentation [MUST]

Use comments, provide explanation on complex algorithms. Unless a function is trivial, always add a high-level comment.

For the documentation, use the [Sphinx style](https://www.sphinx-doc.org/en/master/), which is the official Python standard.

```python
def is_valid(a: int, b: str) -> bool:
    """Explain what the function does

    :param a: what a is
    :type a: int
    :param b: what b is
    :type b: str

    :rtype: bool
    :return: what is the output of the function
    """
```

### Tuples, Lists, Dictionaries [MUST]

Use tuples when data is non-changeable, dictionaries when you need to map things, and lists if your data can change later.

Functions can return multiple values, no need for a list:

```python
def get_info(self) -> str, int:
    """Get the info. No need to return a List/Dict

    :rtype: str, int
    :return: what the str and the int are
    """
    return "hello world", 30
```

### Exceptions handling [MUST]

Hiding an exception or not properly anticipating potential errors (accessing an API for instance, network issues *can- arise) can lead to unexpected behaviors or terminating the execution. Another example is that the caller should be notified if a function receives wrong input parameters to avoid this way wrong results that might be difficult to debug.

Each function has a logic, this logic must be followed by exceptions raised. For instance, if you have a function that get some data from an API, exceptions raised by this function should be logical: connection error, timeout etc. The exception must be raised at the right level of abstraction.

If you choose to propagate the exception to the caller, ensure that you do not expose sensitive information. Tracebacks of exceptions can contain sensitive details leading to exposing intellectual property.

Do not use exceptions as a `go-to` logic, meaning catching an exception and from the `except` calling other business code - the flow of the program will become harder to read. Exceptions are *usually- to notify the caller that something unexpected occured.

Finally, [observability](https://microsoft.github.io/code-with-engineering-playbook/observability/) is an important engineering fundamental. Properly handling exceptions and managing observability (with AppInsight for instance) will lead to a more robust application and easier debugging when something unexpected occurs.

```python
# Never do ...
try:
    process_data()
except:
    pass

# Encapsulate orginal exception trace
def process_data() -> None:
    try:
        do_something()
    except KeyError as e:
        # Raise a specific exception from do_something,
        # encapsulate trace to a custom exception
        raise MyApplicationException("Item not present") from e
```

### Unit tests [MUST]

Unit testing is a core tool in software engineering. They help us verify the correctness of our code, encourage good design practices, and reduce chances to have bugs hitting production. Unit tests can improve development efficiency.

Unit tests should be:

- Reliable: should be 100% reliable so failures indicate a bug in the code.
- Fast: should run in milliseconds.
- Isolated: removing all external dependencies ensures reliability and speed.

`pytest` provides a set of helpful features. Below are some examples:

```python
# Execute this test 3 times, with a, b, and c as input_value
@pytest.mark.parametrize("input_value", ["a", "b", "c"])
def test_(
    input_value
):
    # Test body

# Define a fixed baseline, executed when needed
@pytest.fixture
def items() -> List[str]:
    return ["item 1", "item 2"]

# 'items' will be execute, hence, will be a List[str] with 2 items
def test_items_count(items):
    assert len(items) == 2

```

Please refer to [pytest site](https://docs.pytest.org/en/6.2.x/reference.html) for more useful patterns.

## Use context managers [MUST]

Context managers are tool to use in situations where you need to run some code that has preconditions and postconditions.

For instance, when you read the content of a file, you need to ensure that you close the handle regardless of the success or the failure of the operation. With the `with` keyword you can achieve this:

```python
with open(filename) as fd:
    process_file(fd)

# Note that parentheses are supported in Python 3.10 for context manager,
# useful when you have many 'with'
with (
    CtxManager1() as example1,
    CtxManager2() as example2,
    CtxManager3() as example3,
):
    ...
```

You can implement your own context manager should you need to execute actions in a certain order. Consider the case where you want to update a service configuration. You need first to stop the service, update the configuration then start the service again:

```python
class ServiceHandler:
    def __enter__(self) -> ServiceHandler:
        run("systemctl stop my.service")
        return self

    def __exit__(self, exc_type: str, ex_value: str, ex_traceback: str) -> None:
        run("systemctl start my.service")

def update_service_conf() -> None:
    # Body to update service's configuration

if (__name__ == '__main__'):
    with ServiceHandler():
        update_service_conf()
```
