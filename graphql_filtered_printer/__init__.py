from typing import Any, Mapping, Optional

from .filtering_visitor import FilteringVisitor
from graphql.language.printer import PrintingVisitor

from graphql.language.visitor import visit, ParallelVisitor


class FilteredPrinter:
    __slots__ = ("_filter_arguments",)

    def __init__(self, filter_arguments):
        self._filter_arguments = filter_arguments

    def __call__(self, ast, variables: Optional[Mapping[str, Any]] = None):
        if variables is None:
            variables = {}
        filtering_visitor = FilteringVisitor(self._filter_arguments)
        visitor = ParallelVisitor([filtering_visitor, PrintingVisitor()])
        query = visit(ast, visitor)
        return query, filtering_visitor.filter_variables(variables)
