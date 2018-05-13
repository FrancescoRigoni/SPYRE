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

class CharMatcher:
    """
    Matches a single character.
    """
    def __init__(self, char):
        self.char = char

    def match(self, character):
        return self.char == character


class AnyMatcher:
    """
    Matches any character.
    """
    def __init__(self):
        pass

    def match(self, character):
        return True


class RangeMatcher:
    """
    Matches if a character is included in a range (inclusive) of characters.
    """
    def __init__(self, start_char, end_char):
        self.start_char = start_char
        self.end_char = end_char

    def match(self, character):
        return self.start_char <= character <= self.end_char


class ExcludeRangeMatcher:
    """
    Matches if a character is not included in a range (inclusive) of characters.
    """
    def __init__(self, start_char, end_char):
        self.start_char = start_char
        self.end_char = end_char

    def match(self, character):
        return character < self.start_char or character > self.end_char


class PoolMatcher:
    """
    Matches if a character is included in a set of characters.
    """
    def __init__(self, chars):
        self.chars = chars

    def match(self, character):
        return character in self.chars


class ExcludePoolMatcher:
    """
    Matches if a character is not included in a set of characters.
    """
    def __init__(self, chars):
        self.chars = chars

    def match(self, character):
        return character not in self.chars


class StateMachine:
    state_initial = 0
    state_looping = 1
    state_final = 2
    state_fail = 3

    def __init__(self, matcher):
        self.matcher = matcher
        self.current_state = StateMachine.state_initial
        self.matched_string = ""

    def state_description(self, state):
        return "(" + type(self).__name__ + ": " + str(state) + ")"

    def transition(self, new_state):
        # print("Transition " + self.state_description(self.current_state) +
        # " -> " + self.state_description(new_state))
        self.current_state = new_state

    def reset(self):
        self.current_state = StateMachine.state_initial

    def try_match(self, char):
        if self.matcher.match(char):
            self.matched_string += char
            return True
        else:
            return False

    def is_match(self):
        return self.current_state == StateMachine.state_final

    def is_initial(self):
        return self.current_state == StateMachine.state_initial

    def is_looping(self):
        return self.current_state == StateMachine.state_looping

    def is_fail(self):
        return self.current_state == StateMachine.state_fail

    def start_of_string(self):
        pass

    def end_of_string(self):
        pass

    def process(self, char):
        pass


class StartOfStringStateMachine(StateMachine):
    def __init__(self):
        StateMachine.__init__(self, matcher=None)

    def process(self, char):
        self.transition(StateMachine.state_fail)

    def start_of_string(self):
        if self.current_state == StateMachine.state_initial:
            self.transition(StateMachine.state_final)


class EndOfStringStateMachine(StateMachine):
    def __init__(self):
        StateMachine.__init__(self, matcher=None)

    def process(self, char):
        self.transition(StateMachine.state_fail)

    def end_of_string(self):
        if self.current_state == StateMachine.state_initial:
            self.transition(StateMachine.state_final)


class SingleMatchStateMachine(StateMachine):
    def process(self, character):
        if self.current_state == StateMachine.state_initial:
            if self.try_match(character):
                self.transition(StateMachine.state_final)
            else:
                self.transition(StateMachine.state_fail)


class ZeroOrOneMatchStateMachine(StateMachine):
    def process(self, character):
        if self.current_state == StateMachine.state_initial:
            if self.try_match(character):
                self.transition(StateMachine.state_looping)
            else:
                self.transition(StateMachine.state_final)
        elif self.current_state == StateMachine.state_looping:
            self.transition(StateMachine.state_final)

    def end_of_string(self):
        self.transition(StateMachine.state_final)


class OneOrMoreMatchStateMachine(StateMachine):
    def process(self, character):
        if self.current_state == StateMachine.state_initial:
            if self.try_match(character):
                self.transition(StateMachine.state_looping)
            else:
                self.transition(StateMachine.state_fail)
        elif self.current_state == StateMachine.state_looping:
            if not self.try_match(character):
                self.transition(StateMachine.state_final)

    def end_of_string(self):
        if self.current_state == StateMachine.state_looping:
            self.transition(StateMachine.state_final)
        else:
            self.transition(StateMachine.state_fail)


class ZeroOrMoreMatchStateMachine(StateMachine):
    def process(self, character):
        if self.current_state == StateMachine.state_initial:
            if self.try_match(character):
                self.transition(StateMachine.state_looping)
            else:
                self.transition(StateMachine.state_final)
        elif self.current_state == StateMachine.state_looping:
            if not self.try_match(character):
                self.transition(StateMachine.state_final)

    def end_of_string(self):
        self.transition(StateMachine.state_final)
