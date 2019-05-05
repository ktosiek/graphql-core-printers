import pytest
from graphql.language.parser import parse
from graphql.language.tests.fixtures import KITCHEN_SINK
from graphql_printers import FilteredPrinter


@pytest.fixture(params=["nice", "compact"])
def printer(request):
    return FilteredPrinter(
        filter_arguments=["password", "token"], compact=request.param == "compact"
    )


def test_filtering_inline_password(snapshot, printer):
    ast = parse(
        """
        mutation {
            login(username: "someuser", password: "123456") {
                token
            }
        }
    """
    )

    snapshot.assert_match(printer(ast))


def test_filtering_password_variable(snapshot, printer):
    ast = parse(
        """
        mutation Login($username:String!, $password:String!) {
            login(username: $username, password: $password) {
                token
            }
        }
    """
    )

    snapshot.assert_match(printer(ast, {"username": "someuser", "password": "123456"}))


def test_filtering_shared_variable(snapshot, printer):
    ast = parse(
        """
        mutation Login($username:String!) {
            login(username: $username, password: $username) {
                token
            }
        }
    """
    )

    snapshot.assert_match(printer(ast, {"username": "someuser"}))


def test_filtering_input_object(snapshot, printer):
    ast = parse(
        """
        mutation Login($input:LoginInput!) {
            login(input:$input) {
                token
            }
        }
    """
    )

    snapshot.assert_match(
        printer(ast, {"input": {"username": "someuser", "password": "123456"}})
    )


def test_filtering_variable_shared_with_a_list(snapshot, printer):
    ast = parse(
        """
        mutation Login($password:String!) {
            login(username: "asdf", password: $password) {
                token
            }
            hideArgs(input: ["now you see me", $password]) { __typename }
        }
    """
    )

    snapshot.assert_match(printer(ast, {"password": "123456"}))


def test_filtering_variable_in_a_list(snapshot, printer):
    ast = parse(
        """
        mutation Login($pwd:String!) {
            login(username: "asdf", password: [$pwd]) {
                token
            }
        }
    """
    )

    snapshot.assert_match(printer(ast, {"pwd": "123456"}))


def test_kitchen_sink(benchmark, printer):
    ast = parse(KITCHEN_SINK)
    output, _vars = benchmark(printer, ast, {})
    ast2 = parse(output)
    assert ast == ast2
