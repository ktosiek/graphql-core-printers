# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_kitchen_sink 1'] = {
    'args': (
        'queryName',
        {
            'foo': 'simpleString'
        }
    ),
    'exc_info': None,
    'exc_text': None,
    'filename': 'backends.py',
    'funcName': 'logging_execute',
    'levelname': 'INFO',
    'message': "Executing operation queryName with variables {'foo': 'simpleString'}",
    'module': 'backends',
    'msg': 'Executing operation %s with variables %s',
    'name': 'graphql_printers.backends',
    'operation': 'queryName',
    'query': 'query queryName($foo:ComplexType, $site:Site = MOBILE) {whoever123is:node(id:[123, 456]) {id ... on User @defer {field2 {id alias:field1(first:10, after:$foo) @include(if:$foo) {id ...frag}}} ... @skip(unless:$foo) {id} ... {id}}} mutation likeStory {like(story:123) @defer {story {id}}} subscription StoryLikeSubscription($input:StoryLikeSubscribeInput) {storyLikeSubscribe(input:$input) {story {likers {count} likeSentence {text}}}} fragment frag on Friend {foo(size:$size, bar:$b, obj:{key:"value"})} {unnamed(truthy:true, falsey:false) query}',
    'variables': {
        'foo': 'simpleString'
    }
}

snapshots['test_without_variables 1'] = {
    'args': (
        'queryName',
        {
        }
    ),
    'exc_info': None,
    'exc_text': None,
    'filename': 'backends.py',
    'funcName': 'logging_execute',
    'levelname': 'INFO',
    'message': 'Executing operation queryName with variables {}',
    'module': 'backends',
    'msg': 'Executing operation %s with variables %s',
    'name': 'graphql_printers.backends',
    'operation': 'queryName',
    'query': 'query queryName($foo:ComplexType, $site:Site = MOBILE) {whoever123is:node(id:[123, 456]) {id ... on User @defer {field2 {id alias:field1(first:10, after:$foo) @include(if:$foo) {id ...frag}}} ... @skip(unless:$foo) {id} ... {id}}} mutation likeStory {like(story:123) @defer {story {id}}} subscription StoryLikeSubscription($input:StoryLikeSubscribeInput) {storyLikeSubscribe(input:$input) {story {likers {count} likeSentence {text}}}} fragment frag on Friend {foo(size:$size, bar:$b, obj:{key:"value"})} {unnamed(truthy:true, falsey:false) query}',
    'variables': {
    }
}
