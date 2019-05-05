from typing import Any, Mapping, Optional

from graphql_printers.compact_printing_visitor import CompactPrintingVisitor
from .filtering_visitor import FilteringVisitor
from graphql.language.printer import PrintingVisitor

from graphql.language.visitor import visit, ParallelVisitor


class FilteredPrinter:
    __slots__ = ("_filter_arguments", "_printer_class")

    def __init__(self, filter_arguments, compact=False):
        self._filter_arguments = filter_arguments
        self._printer_class = CompactPrintingVisitor if compact else PrintingVisitor

    def __call__(self, ast, variables: Optional[Mapping[str, Any]] = None):
        if variables is None:
            variables = {}
        filtering_visitor = FilteringVisitor(self._filter_arguments)
        visitor = ParallelVisitor([filtering_visitor, self._printer_class()])
        query = visit(ast, visitor)
        return query, filtering_visitor.filter_variables(variables)


def compact_print_ast(ast):
    return visit(ast, CompactPrintingVisitor())
