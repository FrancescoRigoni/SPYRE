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

from spyre_internals import *


class RegExpParseException(Exception):
    pass


def parse_square_brackets_block(block):
    """
    Example: 0-9, abc
    :param block: the block between square brackets, brackets excluded
    :return: a matcher describing the block
    """
    exclude_chars_in_block = False
    if block[0] == '^':
        # Exclude characters described in this block
        exclude_chars_in_block = True
        block = block[1:]

    if '-' in block:
        for i in range(len(block)):
            if block[i] == '-':
                if 0 < i < len(block)-1:
                    return ExcludeRangeMatcher(block[i-1], block[i+1]) \
                        if exclude_chars_in_block is True \
                        else RangeMatcher(block[i-1], block[i+1])
                else:
                    raise RegExpParseException("parse_square_brackets_block: parse error, malformed block")
    else:
        return ExcludePoolMatcher(block) \
            if exclude_chars_in_block is True \
            else PoolMatcher(block)


def is_frequency_modifier(char):
    return char in ['?', '*', '+']


def lookahead_for_frequency_modifier(regexp, position):
    next_position = position + 1
    if next_position < len(regexp) and is_frequency_modifier(regexp[next_position]):
        return regexp[next_position]


def build_state_machine_with_frequency_modifier(matcher, frequency_modifier):
    if frequency_modifier == '?':
        return ZeroOrOneMatchStateMachine(matcher)
    elif frequency_modifier == '+':
        return OneOrMoreMatchStateMachine(matcher)
    elif frequency_modifier == '*':
        return ZeroOrMoreMatchStateMachine(matcher)
    else:
        return SingleMatchStateMachine(matcher)


def parse_regexp(regexp):
    """
    AKA not the best parsing ever
    Example:
       abc[0-9]+    : literal a, literal b, literal c, range[0-9] one or more times
       abc[abc]*    : literal a, literal b, literal c, a or b or c one or more times
       a+bc[abc]?   : literal a one or more times, literal b, literal c, a or b or c zero or one times

    :param regexp: supports [abcd], [a-z], *,+,?, and literals
    :return: a list of state machines representing the regexp
    """
    escape = None
    current_group = None
    state_machines = []
    for i in range(len(regexp)):
        if regexp[i] == '\\':
            # Consider escape when reading next character
            escape = True
        elif current_group is None:
            if regexp[i] == '[' and not escape:
                current_group = []
            elif regexp[i] == '^' and not escape:
                state_machines.append(StartOfStringStateMachine())
            elif regexp[i] == '$' and not escape:
                state_machines.append(EndOfStringStateMachine())
            elif not is_frequency_modifier(regexp[i]):
                if regexp[i] == '.' and not escape:
                    matcher = AnyMatcher()
                else:
                    matcher = CharMatcher(regexp[i])

                frequency_modifier = lookahead_for_frequency_modifier(regexp, i)
                state_machine = build_state_machine_with_frequency_modifier(matcher, frequency_modifier)
                state_machines.append(state_machine)
            elif is_frequency_modifier(regexp[i]):
                # Check for consecutive frequency modifiers, which are not supported
                frequency_modifier = lookahead_for_frequency_modifier(regexp, i)
                if frequency_modifier is not None:
                    raise RegExpParseException("Unexpected frequency modifier in regexp " +
                                    regexp + " at position " + str(i))

        elif current_group is not None:
            if regexp[i] == ']' and not escape:
                frequency_modifier = lookahead_for_frequency_modifier(regexp, i)
                matcher = parse_square_brackets_block(current_group)
                state_machine = build_state_machine_with_frequency_modifier(matcher, frequency_modifier)
                state_machines.append(state_machine)
                current_group = None
            else:
                current_group.append(regexp[i])

    if current_group is not None:
        # Unclosed square brackets
        raise RegExpParseException("Unclosed square brackets in regexp")

    return state_machines
