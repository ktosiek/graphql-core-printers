# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_filtering_inline_password[nice] 1'] = (
    '''mutation {
  login(username: "someuser", password: "[FILTERED]") {
    token
  }
}
''',
    {
    }
)

snapshots['test_filtering_password_variable[nice] 1'] = (
    '''mutation Login($username: String!, $password: String!) {
  login(username: $username, password: $password) {
    token
  }
}
''',
    {
        'password': '[FILTERED]',
        'username': 'someuser'
    }
)

snapshots['test_filtering_shared_variable[nice] 1'] = (
    '''mutation Login($username: String!) {
  login(username: $username, password: $username) {
    token
  }
}
''',
    {
        'username': 'someuser'
    }
)

snapshots['test_filtering_input_object[nice] 1'] = (
    '''mutation Login($input: LoginInput!) {
  login(input: $input) {
    token
  }
}
''',
    {
        'input': {
            'password': '[FILTERED]',
            'username': 'someuser'
        }
    }
)

snapshots['test_filtering_variable_shared_with_a_list[nice] 1'] = (
    '''mutation Login($password: String!) {
  login(username: "asdf", password: $password) {
    token
  }
  hideArgs(input: ["now you see me", $password]) {
    __typename
  }
}
''',
    {
        'password': '123456'
    }
)

snapshots['test_filtering_variable_in_a_list[nice] 1'] = (
    '''mutation Login($pwd: String!) {
  login(username: "asdf", password: [$pwd]) {
    token
  }
}
''',
    {
        'pwd': '[FILTERED]'
    }
)

snapshots['test_filtering_inline_password[compact] 1'] = (
    'mutation {login(username:"someuser", password:"[FILTERED]") {token}}',
    {
    }
)

snapshots['test_filtering_password_variable[compact] 1'] = (
    'mutation Login($username:String!, $password:String!) {login(username:$username, password:$password) {token}}',
    {
        'password': '[FILTERED]',
        'username': 'someuser'
    }
)

snapshots['test_filtering_shared_variable[compact] 1'] = (
    'mutation Login($username:String!) {login(username:$username, password:$username) {token}}',
    {
        'username': 'someuser'
    }
)

snapshots['test_filtering_input_object[compact] 1'] = (
    'mutation Login($input:LoginInput!) {login(input:$input) {token}}',
    {
        'input': {
            'password': '[FILTERED]',
            'username': 'someuser'
        }
    }
)

snapshots['test_filtering_variable_shared_with_a_list[compact] 1'] = (
    'mutation Login($password:String!) {login(username:"asdf", password:$password) {token} hideArgs(input:["now you see me", $password]) {__typename}}',
    {
        'password': '123456'
    }
)

snapshots['test_filtering_variable_in_a_list[compact] 1'] = (
    'mutation Login($pwd:String!) {login(username:"asdf", password:[$pwd]) {token}}',
    {
        'pwd': '[FILTERED]'
    }
)
