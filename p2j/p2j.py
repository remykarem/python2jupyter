"""
This module translates .py files to .ipynb and vice versa
"""
import argparse
import os
import json
import sys

# Path to directory
HERE = os.path.abspath(os.path.dirname(__file__))

RESERVED = ['for', 'with', 'class', 'while']  # reserved Python keywords
TRIPLE_QUOTES = ["\"\"\"", "\'\'\'"]
FOUR_SPACES = "{:<4}".format("")
EIGHT_SPACES = "{:<8}".format("")
TWELVE_SPACES = "{:<12}".format("")


def p2j(source_filename, target_filename, overwrite):
    """Convert Python scripts to Jupyter notebooks.

    Args:
        source_filename (str): Path to Python script.
        target_filename (str): Path to name of Jupyter notebook. Optional.
        overwrite (bool): Whether to overwrite an existing Jupyter notebook.
    """

    # Check if source file exists and read
    file_ext = os.path.splitext(source_filename)[-1]
    if file_ext != ".py":
        print("Wrong file type specified. Expected .ipynb extension " +
              "but got {} instead.".format(file_ext))
        sys.exit(1)
    try:
        with open(source_filename, 'r') as infile:
            data = [l.rstrip('\n') for l in infile]
    except FileNotFoundError:
        print("Source file not found. Specify a valid source file.")
        sys.exit(1)

    # Check if target file is specified and exists. If not specified, create
    if target_filename is None:
        target_filename = os.path.splitext(source_filename)[0] + ".ipynb"
    if not overwrite and os.path.isfile(target_filename):
        # FileExistsError
        print("File {} exists. ".format(target_filename) +
              "Add -o flag to overwrite this file, " +
              "or specify a different target filename using -t.")
        sys.exit(1)

    # Read JSON files for .ipynb template
    with open(HERE + '/templates/cell_code.json') as file:
        CODE = json.load(file)
    with open(HERE + '/templates/cell_markdown.json') as file:
        MARKDOWN = json.load(file)
    with open(HERE + '/templates/metadata.json') as file:
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
        is_code = line.startswith("# pylint") or line.startswith(
            "#pylint") or line.startswith("#!") or line.startswith(
                "# -*- coding") or line.startswith("# coding=") or line.startswith(
                    "# This Python file uses the following encoding:")
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
                buffer = buffer[2:]

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
    with open(target_filename, 'w') as outfile:
        json.dump(final, outfile)
        print("Notebook {} written.".format(target_filename))


def j2p(source_filename, target_filename, overwrite):
    """Convert Jupyter notebooks to Python scripts

    Args:
        source_filename (str): Path to Jupyter notebook.
        target_filename (str): Path to name of Python script. Optional.
        overwrite (bool): Whether to overwrite an existing Python script.
        with_markdown (bool, optional): Whether to include markdown. Defaults to False.
    """

    # Check if source file exists and read
    file_ext = os.path.splitext(source_filename)[-1]
    if file_ext != ".ipynb":
        print("Wrong file type specified. Expected .ipynb extension " +
              "but got {} instead.".format(file_ext))
        sys.exit(1)
    try:
        with open(source_filename, 'r') as infile:
            myfile = json.load(infile)
    except FileNotFoundError:
        print("Source file not found. Specify a valid source file.")
        sys.exit(1)

    # Check if target file is specified and exists. If not specified, create
    if target_filename is None:
        target_filename = os.path.splitext(source_filename)[0] + ".py"
    if not overwrite and os.path.isfile(target_filename):
        # FileExistsError
        print("File {} exists. ".format(target_filename) +
              "Add -o flag to overwrite this file, " +
              "or specify a different target filename using -t.")
        sys.exit(1)

    final = [''.join(["# " + line.lstrip() for line in cell["source"] if not line.strip() == ""])
             if cell["cell_type"] == "markdown" else ''.join(cell["source"])
             for cell in myfile['cells']]
    final = '\n\n'.join(final)
    final = final.replace("<br>", "")

    with open(target_filename, "a") as outfile:
        outfile.write(final)
        print("Python script {} written.".format(target_filename))


def main():

    # Get source and target filenames
    parser = argparse.ArgumentParser(
        description='Convert a Python script to Jupyter notebook and vice versa')
    parser.add_argument('source_filename',
                        help='Python script to parse')
    parser.add_argument('-r',
                        '--reverse',
                        action='store_true',
                        help="To convert Jupyter to Python scripto")
    parser.add_argument('-t',
                        '--target_filename',
                        help="Target filename of Jupyter notebook. If not specified, " +
                        "it will use the filename of the Python script and append .ipynb")
    parser.add_argument('-o',
                        '--overwrite',
                        action='store_true',
                        help='Flag whether to overwrite existing target file. Defaults to false')
    args = parser.parse_args()

    if args.reverse:
        j2p(source_filename=args.source_filename,
            target_filename=args.target_filename,
            overwrite=args.overwrite)
    else:
        p2j(source_filename=args.source_filename,
            target_filename=args.target_filename,
            overwrite=args.overwrite)


if __name__ == "__main__":
    main()
