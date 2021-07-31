"""
This module translates .py files to .ipynb and vice versa
"""
from typing import Optional
import os
import sys
import json

from p2j.utils import _check_files

# Path to directory
HERE = os.path.abspath(os.path.dirname(__file__))

TRIPLE_QUOTES = ["\"\"\"", "\'\'\'"]
FOUR_SPACES = "{:<4}".format("")
EIGHT_SPACES = "{:<8}".format("")
TWELVE_SPACES = "{:<12}".format("")


def python2jupyter(source_filename: str, target_filename: str, overwrite: bool = False):
    """Convert Python scripts to Jupyter notebooks.

    Args:
        source_filename (str): Path to Python script.
        target_filename (str): Path to name of Jupyter notebook. Optional.
        overwrite (bool): Whether to overwrite an existing Jupyter notebook.
    """

    target_filename = _check_files(
        source_filename, target_filename, overwrite, conversion="p2j")

    # Check if source file exists and read
    try:
        with open(source_filename, "r", encoding="utf-8") as infile:
            data = [l.rstrip("\n") for l in infile]
    except FileNotFoundError:
        print("Source file not found. Specify a valid source file.")
        sys.exit(1)

    # Read JSON files for .ipynb template
    with open(HERE + "/templates/cell_code.json", encoding="utf-8") as file:
        CODE = json.load(file)
    with open(HERE + "/templates/cell_markdown.json", encoding="utf-8") as file:
        MARKDOWN = json.load(file)
    with open(HERE + "/templates/metadata.json", encoding="utf-8") as file:
        MISC = json.load(file)

    # Initialise variables
    final = {}              # the dictionary/json of the final notebook
    cells = []              # an array of all markdown and code cells
    arr = []                # an array to store individual lines for a cell
    num_lines = len(data)   # no. of lines of code

    # Initialise variables for checks
    is_block_comment = False
    is_running_code = False
    is_running_comment = False
    next_is_code = False
    next_is_nothing = False
    next_is_function = False

    # Read source code line by line
    for i, line in enumerate(data):

        # Skip if line is empty
        if line == "":
            continue

        buffer = ""

        # Labels for current line
        contains_triple_quotes = TRIPLE_QUOTES[0] in line or TRIPLE_QUOTES[1] in line
        is_code = line.startswith("# pylint") or line.startswith("#pylint") or \
            line.startswith("#!") or line.startswith("# -*- coding") or \
            line.startswith("# coding=") or line.startswith("##") or \
            line.startswith("# FIXME") or line.startswith("#FIXME") or \
            line.startswith("# TODO") or line.startswith("#TODO") or \
            line.startswith("# This Python file uses the following encoding:")
        is_end_of_code = i == num_lines-1
        starts_with_hash = line.startswith("#")

        # Labels for next line
        try:
            next_is_code = not data[i+1].startswith("#")
        except IndexError:
            pass
        try:
            next_is_nothing = data[i+1] == ""
        except IndexError:
            pass
        try:
            next_is_function = data[i+1].startswith(FOUR_SPACES) or (
                next_is_nothing and data[i+2].startswith(FOUR_SPACES))
        except IndexError:
            pass

        # Sub-paragraph is a comment but not a running code
        if not is_running_code and (is_running_comment or
                                    (starts_with_hash and not is_code) or
                                    contains_triple_quotes):

            if contains_triple_quotes:
                is_block_comment = not is_block_comment

            buffer = line.replace(TRIPLE_QUOTES[0], "\n").\
                replace(TRIPLE_QUOTES[1], "\n")

            if not is_block_comment:
                if len(buffer) > 1:
                    buffer = buffer[2:] if buffer[1].isspace() else buffer[1:]
                else:
                    buffer = ""

            # Wrap this sub-paragraph as a markdown cell if
            # next line is end of code OR
            # (next line is a code but not a block comment) OR
            # (next line is nothing but not a block comment)
            if is_end_of_code or (next_is_code and not is_block_comment) or \
                    (next_is_nothing and not is_block_comment):
                arr.append("{}".format(buffer))
                MARKDOWN["source"] = arr
                cells.append(dict(MARKDOWN))
                arr = []
                is_running_comment = False
            else:
                buffer = buffer + "<br>\n"
                arr.append("{}".format(buffer))
                is_running_comment = True
                continue
        else:  # Sub-paragraph is a comment but not a running code
            buffer = line

            # Wrap this sub-paragraph as a code cell if
            # (next line is end of code OR next line is nothing) AND NOT
            # (next line is nothing AND next line is part of a function)
            if (is_end_of_code or next_is_nothing) and not (next_is_nothing and next_is_function):
                arr.append("{}".format(buffer))
                CODE["source"] = arr
                cells.append(dict(CODE))
                arr = []
                is_running_code = False
            else:
                buffer = buffer + "\n"

                # Put another newline character if in a function
                try:
                    if data[i+1] == "" and (data[i+2].startswith("    #") or
                                            data[i+2].startswith("        #") or
                                            data[i+2].startswith("            #")):
                        buffer = buffer + "\n"
                except IndexError:
                    pass

                arr.append("{}".format(buffer))
                is_running_code = True
                continue

    # Finalise the contents of notebook
    final["cells"] = cells
    final.update(MISC)

    # Write JSON to target file
    with open(target_filename, "w", encoding="utf-8") as outfile:
        json.dump(final, outfile, indent=1, ensure_ascii=False)
        print("Notebook {} written.".format(target_filename))
