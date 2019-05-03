from typing import Any, Mapping, Optional

from .filtering_visitor import FilteringVisitor

from graphql.language.visitor import visit


class FilteredPrinter:
    __slots__ = ("_filter_arguments",)

    def __init__(self, filter_arguments):
        self._filter_arguments = filter_arguments

    def __call__(self, ast, variables: Optional[Mapping[str, Any]] = None):
        if variables is None:
            variables = {}
        visitor = FilteringVisitor(self._filter_arguments)
        query = visit(ast, visitor)
        return query, visitor.filter_variables(variables)
