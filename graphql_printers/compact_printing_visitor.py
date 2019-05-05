import json

from graphql.language.printer import PrintingVisitor, join, wrap


class CompactPrintingVisitor(PrintingVisitor):
    def leave_Document(self, node, *args):
        # type: (Any, *Any) -> str
        return join(node.definitions, " ")

    def leave_OperationDefinition(self, node, *args):
        # type: (Any, *Any) -> str
        name = node.name
        selection_set = node.selection_set
        op = node.operation
        var_defs = wrap("(", join(node.variable_definitions, ", "), ")")
        directives = join(node.directives, " ")

        if not name and not directives and not var_defs and op == "query":
            return selection_set

        return join([op, join([name, var_defs]), directives, selection_set], " ")

    def leave_VariableDefinition(self, node, *args):
        # type: (Any, *Any) -> str
        return node.variable + ":" + node.type + wrap(" = ", node.default_value)

    def leave_SelectionSet(self, node, *args):
        # type: (Any, *Any) -> str
        return block(node.selections)

    def leave_Field(self, node, *args):
        # type: (Any, *Any) -> str
        return join(
            [
                wrap("", node.alias, ":")
                + node.name
                + wrap("(", join(node.arguments, ", "), ")"),
                join(node.directives, " "),
                node.selection_set,
            ],
            " ",
        )

    def leave_Argument(self, node, *args):
        # type: (Any, *Any) -> str
        return "{0.name}:{0.value}".format(node)

    # Value

    def leave_ListValue(self, node, *args):
        # type: (Any, *Any) -> str
        return "[" + join(node.values, ", ") + "]"

    def leave_ObjectValue(self, node, *args):
        # type: (Any, *Any) -> str
        return "{" + join(node.fields, ", ") + "}"

    def leave_ObjectField(self, node, *args):
        # type: (Any, *Any) -> str
        return node.name + ":" + node.value

    # Directive

    def leave_Directive(self, node, *args):
        # type: (Any, *Any) -> str
        return "@" + node.name + wrap("(", join(node.arguments, ", "), ")")


def block(_list):
    # type: (List[str]) -> str
    if _list:
        return "{" + join(_list, " ") + "}"
    return "{}"
