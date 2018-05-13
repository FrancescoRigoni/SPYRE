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


def remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s


def match_regexp(regexp, string):
    state_machines = parse_regexp(regexp)
    matched_string = None
    current_sm = 0
    current_char = 0

    while current_sm < len(state_machines):
        # The following conditional block deals with sending the meta events to the current
        # state machine (start of string, end of string, ...)
        if current_char == 0 and current_sm == 0:
            # Propagate start of string event
            state_machines[current_sm].start_of_string()

        if current_char == len(string):
            # If end of string is reached, all remaining state machines have to be informed
            # So they can succeed (for optional matches) or fail (for mandatory matches)
            # Check is performed at the beginning to correctly handle an empty string
            [sm.end_of_string() for sm in state_machines[current_sm:]]
            break

        # The following conditional block deals with checking the status of the current state machine
        # after the meta events from the first conditional are processed.
        # Characters events are processed here.
        if state_machines[current_sm].is_initial():
            # Process next character
            state_machines[current_sm].process(string[current_char])

            # If the first state machine fails processing the very first character
            # then it is not considered as a failure, that state machine gets reset and the not maching
            # character is removed from the string.
            # This is to allow matching in a position different than the very beginning of the
            # string.
            if state_machines[current_sm].is_fail() and current_char == 0 and current_sm == 0:
                state_machines[current_sm].reset()
                string = string[1:]
            else:
                # Otherwise proceed to the next character
                current_char = current_char + 1

        elif state_machines[current_sm].is_looping():
            # Still looping, go on to the next character
            state_machines[current_sm].process(string[current_char])
            current_char = current_char + 1
        elif state_machines[current_sm].is_match():
            # When a match is found, remove the matched string from the beginning of
            # the main string
            string = remove_prefix(string, state_machines[current_sm].matched_string)
            # The go on to the next state machine and reset the char position since the
            # prefix has been removed
            current_sm = current_sm + 1
            current_char = 0
        elif state_machines[current_sm].is_fail():
            # Or just exit if the current state machine failed
            break

    # Check if all machines match and build the matched string
    if all(state_machine.is_match() for state_machine in state_machines):
        matched_string = ""
        for sm in state_machines:
            matched_string += sm.matched_string

    return matched_string
