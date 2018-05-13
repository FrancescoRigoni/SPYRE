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

from spyre_engine import *


def test_regexps_basic():
    assert match_regexp("a", "ab") == "a"
    assert match_regexp("a", "a") == "a"
    assert match_regexp("a", "") is None

    assert match_regexp("ab", "abc") == "ab"
    assert match_regexp("ab", "ab") == "ab"
    assert match_regexp("ab", "a") is None
    assert match_regexp("ab", "") is None

    assert match_regexp("abc", "abc") == "abc"
    assert match_regexp("abc", "ab") is None
    assert match_regexp("abc", "abcd") == "abc"

    assert match_regexp("a+", "") is None
    assert match_regexp("a+", "a") == "a"

    assert match_regexp("a+", "aa") == "aa"
    assert match_regexp("a+", "aaa") == "aaa"

    assert match_regexp("a*", "") == ""
    assert match_regexp("a*", "a") == "a"
    assert match_regexp("a*", "aa") == "aa"
    assert match_regexp("a*", "aaa") == "aaa"


def test_regexps_complex():
    for i in range(10):
        assert match_regexp("[0-9]", str(i)) == str(i)

    for i in range(1, 2):
        test_string = str(i) * i
        assert match_regexp("[0-9]?", test_string) == test_string

    for c in range(10):
        for i in range(10):
            test_string = str(c) * i
            assert match_regexp("[0-9]*", test_string) == test_string

    for c in range(10):
        for i in range(1, 10):
            test_string = str(c) * i
            assert match_regexp("[0-9]+", test_string) == test_string

    test_string = "abcdabcdefghi"
    assert match_regexp("abcd[0-9]+[a-z]*", test_string) is None

    test_string = "abcd0123456789"
    assert match_regexp("abcd[0-9]+[a-z]*", test_string) == test_string

    test_string = "abcd0123456789abcdefghi"
    match_regexp("abcd[0-9]+[a-z]*", test_string)
    assert match_regexp("abcd[0-9]+[a-z]*", test_string) == test_string

    test_string = "abcdabcdefghi"
    assert match_regexp("abcd[0-9]?[a-z]*", test_string) == test_string

    test_string = "abcdabcdefghi"
    assert match_regexp("abcd[a-z]*", test_string) == test_string

    test_string = "abcda1984"
    assert match_regexp("[a-z]*[1-9][1-9]8[1-9]", test_string) == test_string

    test_string = "abcda1984"
    assert match_regexp("^[a-z]*[1-9][1-9]8[1-9]", test_string) == test_string

    test_string = "123456"
    assert match_regexp("[^a-z]*", test_string) == test_string

    test_string = "abcdabcdefghi"
    assert match_regexp("abcd[^0-9]+[^a-z]*", test_string) == test_string

    test_string = "abcd[0-9]"
    assert match_regexp("abcd\[0-9]", test_string) == test_string


def test_regexps_not_at_start_of_string():
    test_string = "_-_-_-_-_abcd0"
    assert match_regexp("abcd0", test_string) == "abcd0"


def test_regexps_start_of_string():
    test_string = "abcd0"
    assert match_regexp("^abcd0", test_string) == test_string


def test_regexps_start_of_string_fail():
    test_string = "_abcd0"
    match_regexp("^abcd0", test_string)
    assert match_regexp("^abcd0", test_string) is None


def test_regexps_start_of_string_escaped():
    test_string = "^abcd0"
    assert match_regexp("\^abcd0", test_string) == test_string


def test_regexps_not_at_end_of_string():
    test_string = "abcd0_-_-_-"
    assert match_regexp("abcd0", test_string) == "abcd0"


def test_regexps_end_of_string():
    test_string = "abcd0"
    assert match_regexp("abcd0$", test_string) == test_string


def test_regexps_end_of_string_fail():
    test_string = "abcd01"
    assert match_regexp("abcd0$", test_string) is None


def test_regexps_end_of_string_escaped():
    test_string = "abcd0$"
    assert match_regexp("abcd0\$", test_string) == test_string


def test_regexps_any_match():
    test_string = "a"
    assert match_regexp(".", test_string) == test_string

    test_string = "aa"
    assert match_regexp(".", test_string) == 'a'

    test_string = "abcd&1991"
    assert match_regexp("^abcd.[0-9]+", test_string) == test_string

    test_string = "abcd&"
    assert match_regexp("^abcd.+", test_string) == test_string

    test_string = "abcd&&&"
    assert match_regexp("^abcd.+", test_string) == test_string

    test_string = "abcd"
    assert match_regexp("^abcd.?", test_string) == test_string

    test_string = "abcd&"
    assert match_regexp("^abcd.?", test_string) == test_string

    test_string = "abcd&&"
    assert match_regexp("^abcd.?", test_string) == 'abcd&'

    test_string = "abcd"
    assert match_regexp("^abcd.*", test_string) == test_string

    test_string = "abcd&"
    assert match_regexp("^abcd.*", test_string) == test_string

    test_string = "abcd&&&"
    assert match_regexp("^abcd.*", test_string) == test_string

    test_string = "abcd."
    assert match_regexp("^abcd[.]", test_string) == test_string

    test_string = "abcda"
    assert match_regexp("^abcd[.a]", test_string) == test_string

    test_string = "abcd."
    assert match_regexp("^abcd\.", test_string) == test_string
