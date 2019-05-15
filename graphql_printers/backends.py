import logging
from functools import wraps

from graphql import GraphQLBackend, GraphQLDocument

from graphql_printers import FilteredPrinter


class LoggingGraphQLBackendMixin(GraphQLBackend):
    def __init__(self, *args, logger=None, query_printer=None, **kwargs):
        self._query_printer = query_printer or FilteredPrinter(filter_arguments=['token', 'password'], compact=True)
        self._logger = logger or logging.getLogger(__name__)
        super().__init__(*args, **kwargs)

    def document_from_string(self, schema, request_string):
        document: GraphQLDocument = super().document_from_string(schema, request_string)
        document.execute = self._prepare_execute(document)
        return document

    def _prepare_execute(self, document):
        execute = document.execute
        @wraps(execute)
        def logging_execute(**kwargs):
            operation_name = kwargs['operation_name']
            filtered_query, filtered_variables = self._query_printer(document.document_ast, kwargs['variables'])

            self._logger.info(
                'Executing operation %s with variables %s',
                operation_name, filtered_variables,
                extra={
                    'query': filtered_query,
                    'variables': filtered_variables,
                    'operation': operation_name,
                })

            return execute(**kwargs)

        return logging_execute
