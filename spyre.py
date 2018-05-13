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

import test_parser
import test_regexps
import inspect


if __name__ == "__main__":
    parser_tests = inspect.getmembers(test_parser, inspect.isfunction)
    for key, value in parser_tests:
        if key.startswith("test_"):
            print("Running: " + key)
            value()

    regexps_tests = inspect.getmembers(test_regexps, inspect.isfunction)
    for key, value in regexps_tests:
        if key.startswith("test_"):
            print("Running: " + key)
            value()


