from graphql.language.parser import parse

from graphql_filtered_printer import FilteredPrinter

from .schema import Schema


printer = FilteredPrinter(filter_arguments=["password", "token"])


def test_filtering_inline_password(snapshot):
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


def test_filtering_password_variable(snapshot):
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


def test_filtering_shared_variable(snapshot):
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


def test_filtering_input_object(snapshot):
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
