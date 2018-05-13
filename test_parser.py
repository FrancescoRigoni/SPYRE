#!/usr/bin/python3

"""
SPYRE - Simple PYthon 3 Regular Expression Engine
Copyright (C) 2018 Francesco Rigoni - francesco.rigoni@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from spyre_parser import *


def test_parse_square_brackets_block_simple_pool_matcher():
    matcher = parse_square_brackets_block("abcd")
    assert type(matcher) == PoolMatcher
    assert matcher.chars == "abcd"


def test_parse_square_brackets_block_simple_range_matcher():
    matcher = parse_square_brackets_block("a-d")
    assert type(matcher) == RangeMatcher
    assert matcher.start_char == 'a'
    assert matcher.end_char == 'd'


def test_parse_regexp_1():
    state_machines = parse_regexp("abc[0-9]+")
    assert type(state_machines[0]) == SingleMatchStateMachine
    assert state_machines[0].matcher.char == 'a'
    assert type(state_machines[1]) == SingleMatchStateMachine
    assert state_machines[1].matcher.char == 'b'
    assert type(state_machines[2]) == SingleMatchStateMachine
    assert state_machines[2].matcher.char == 'c'
    assert type(state_machines[3]) == OneOrMoreMatchStateMachine
    assert type(state_machines[3].matcher) == RangeMatcher
    assert state_machines[3].matcher.start_char == '0'
    assert state_machines[3].matcher.end_char == '9'


def test_parse_regexp_2():
    state_machines = parse_regexp("a*b")
    assert type(state_machines[0]) == ZeroOrMoreMatchStateMachine
    assert state_machines[0].matcher.char == 'a'
    assert type(state_machines[1]) == SingleMatchStateMachine
    assert state_machines[1].matcher.char == 'b'


def test_parse_regexp_3():
    state_machines = parse_regexp("a*b+")
    assert type(state_machines[0]) == ZeroOrMoreMatchStateMachine
    assert state_machines[0].matcher.char == 'a'
    assert type(state_machines[1]) == OneOrMoreMatchStateMachine
    assert state_machines[1].matcher.char == 'b'


def test_parse_regexp_4():
    state_machines = parse_regexp("[0123]?")
    assert type(state_machines[0]) == ZeroOrOneMatchStateMachine
    assert type(state_machines[0].matcher) == PoolMatcher
    assert state_machines[0].matcher.chars == list('0123')


def test_parse_regexp_5():
    state_machines = parse_regexp("[[]]?")
    assert type(state_machines[0]) == SingleMatchStateMachine
    assert type(state_machines[0].matcher) == PoolMatcher
    assert state_machines[0].matcher.chars == list('[')
    assert type(state_machines[1]) == ZeroOrOneMatchStateMachine
    assert type(state_machines[1].matcher) == CharMatcher
    assert state_machines[1].matcher.char == ']'


def test_parse_regexp_unopened_square_brackets():
    state_machines = parse_regexp("\[0-9]")
    assert type(state_machines[0]) == SingleMatchStateMachine
    assert state_machines[0].matcher.char == '['
    assert type(state_machines[1]) == SingleMatchStateMachine
    assert state_machines[1].matcher.char == '0'
    assert type(state_machines[2]) == SingleMatchStateMachine
    assert state_machines[2].matcher.char == '-'
    assert type(state_machines[3]) == SingleMatchStateMachine
    assert state_machines[3].matcher.char == '9'
    assert type(state_machines[4]) == SingleMatchStateMachine
    assert state_machines[4].matcher.char == ']'


def test_parse_regexp_unclosed_square_brackets():
    try:
        parse_regexp("[0-9")
        assert False
    except RegExpParseException:
        pass


def test_parse_regexp_unclosed_square_brackets_escaped():
    try:
        parse_regexp("[0-9\]")
        assert False
    except RegExpParseException:
        pass
