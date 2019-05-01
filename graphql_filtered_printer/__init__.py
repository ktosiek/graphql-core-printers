from typing import Any, Mapping, Optional

from collections import defaultdict
from graphql.language.printer import PrintingVisitor, join, wrap
from graphql.language.visitor import visit

import json


class FilteredPrinter:
    __slots__ = ("_filter_arguments",)

    def __init__(self, filter_arguments):
        self._filter_arguments = filter_arguments

    def __call__(self, ast, variables: Optional[Mapping[str, Any]] = None):
        if variables is None:
            variables = {}
        visitor = FilteringVisitor(self._filter_arguments, variables.keys())
        query = visit(ast, visitor)
        return query, visitor.filter_variables(variables)


class FilteringVisitor(PrintingVisitor):
    __slots__ = ("_filter_arguments", "_variable_uses", "_tainted_uses")

    def __init__(self, filter_arguments, variable_names):
        self._filter_arguments = set(filter_arguments)
        self._variable_uses = defaultdict(int)
        self._tainted_uses = defaultdict(int)

    def filter_variables(self, variables):
        return {
            k: "[FILTERED]" if self.variable_is_tainted(k) else self._filter_value(v)
            for k, v in variables.items()
        }

    def _filter_value(self, value):
        if isinstance(value, dict):
            return {
                k: "[FILTERED]" if self._should_filter(k) else self._filter_value(v)
                for k, v in value.items()
            }
        if isinstance(value, list):
            return [self._filter_value(v) for v in value]
        return value

    def variable_is_tainted(self, name):
        # If variable was used in both filtered and unfiltered position assume it's not a secret
        tainted_uses = self._tainted_uses[name]
        return tainted_uses and tainted_uses == self._variable_uses[name]

    def leave_Variable(self, node, *args):
        self._variable_uses[node.name] += 1
        return super().leave_Variable(node, *args)

    def enter_VariableDefinition(self, node, *args):
        # compensate for leave_Variable inside the VariableDefinition
        var_name = node.variable.name.value
        self._variable_uses[var_name] -= 1

    def leave_Argument(self, node, *args):
        # type: (Any, *Any) -> str
        value = node.value
        if self._should_filter(node.name):
            if node.value.startswith("$"):
                self._tainted_uses[node.value[1:]] += 1
            else:
                value = '"[FILTERED]"'
        return "{0.name}: {1}".format(node, value)

    def leave_ObjectField(self, node, *args):
        # type: (Any, *Any) -> str
        return node.name + ": " + node.value

    def _should_filter(self, arg_name):
        return arg_name in self._filter_arguments
