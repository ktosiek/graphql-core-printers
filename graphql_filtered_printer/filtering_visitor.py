from collections import defaultdict

from graphql.language.visitor import Visitor


class FilteringVisitor(Visitor):
    __slots__ = (
        "_filter_arguments",
        "_variable_uses",
        "_tainted_uses",
        "_tainted_context",
    )

    def __init__(self, filter_arguments):
        self._filter_arguments = set(filter_arguments)
        self._variable_uses = defaultdict(int)
        self._tainted_uses = defaultdict(int)
        self._tainted_context = False

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
        if self._tainted_context:
            self._tainted_uses[node.name] += 1

    def enter_VariableDefinition(self, node, *args):
        # compensate for leave_Variable inside the VariableDefinition
        var_name = node.variable.name.value
        self._variable_uses[var_name] -= 1

    def enter_Argument(self, node, *args):
        if self._should_filter(node.name.value):
            self._tainted_context = True

    def leave_Argument(self, node, *args):
        self._tainted_context = False

    def leave_StringValue(self, node, *args):
        if self._tainted_context:
            return '"[FILTERED]"'

    def _should_filter(self, arg_name):
        return arg_name in self._filter_arguments
