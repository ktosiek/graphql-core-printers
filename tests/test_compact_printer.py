from graphql import parse
from graphql.language.tests.fixtures import KITCHEN_SINK

from graphql_printers import compact_print_ast


def test_kitchen_sink():
    ast = parse(KITCHEN_SINK)
    output = compact_print_ast(ast)
    assert len(output.splitlines()) == 1
