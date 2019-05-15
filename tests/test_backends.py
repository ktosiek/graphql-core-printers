import logging

import pytest
from graphql import GraphQLBackend, GraphQLDocument, parse
from graphql.language.tests.fixtures import KITCHEN_SINK

from graphql_printers.backends import LoggingGraphQLBackendMixin


class MockBackend(GraphQLBackend):
    def document_from_string(self, schema, request_string):
        return GraphQLDocument(schema, request_string, parse(request_string), execute=lambda **kwargs: None)


class Backend(LoggingGraphQLBackendMixin, MockBackend):
    pass


@pytest.fixture
def snapshot_log_record(snapshot):
    return lambda r: snapshot.assert_match({
        'args': r.args,
        'exc_info': r.exc_info,
        'exc_text': r.exc_text,
        'filename': r.filename,
        'funcName': r.funcName,
        'levelname': r.levelname,
        'message': r.message,
        'module': r.module,
        'msg': r.msg,
        'name': r.name,
        'operation': r.operation,
        'query': r.query,
        'variables': r.variables,
    })


def test_kitchen_sink(caplog, snapshot_log_record):
    caplog.set_level(logging.INFO)
    document = Backend().document_from_string(None, KITCHEN_SINK)
    document.execute(
        operation_name='queryName',
        variables={'foo': 'simpleString'},
    )
    assert len(caplog.records) == 1
    r = caplog.records[0]
    snapshot_log_record(r)


def test_without_variables(caplog, snapshot_log_record):
    caplog.set_level(logging.INFO)
    document = Backend().document_from_string(None, KITCHEN_SINK)
    document.execute(
        operation_name='queryName',
        variables=None,
    )
    assert len(caplog.records) == 1
    r = caplog.records[0]
    snapshot_log_record(r)
