"""
This code translates .py files to .ipynb
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


def p2j_(source_filename, target_filename, overwrite):

    # Check if source file exists and read
    try:
        with open(source_filename, 'r') as file:
            data = [l.rstrip('\n') for l in file]
    except FileNotFoundError:
        print("Source file not found. Specify a valid source file.")
        sys.exit(1)

    # Check if target file is specified and exists. If not specified, create
    if target_filename is None:
        target_filename = os.path.splitext(source_filename)[0] + ".ipynb"
    if not overwrite and os.path.isfile(target_filename):
        print("File {} exists. Add -o flag to overwrite this file,".format(target_filename) +
              " or specify a different name.")
        sys.exit(1)

    # Read JSON files for .ipynb template
    with open(HERE + '/templates/cell_code.json') as file:
        code = json.load(file)
    with open(HERE + '/templates/cell_markdown.json') as file:
        markdown = json.load(file)
    with open(HERE + '/templates/metadata.json') as file:
        misc = json.load(file)

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
        if not is_running_code and (
            is_running_comment or (
                starts_with_hash and not is_code) or contains_triple_quotes
        ):

            if contains_triple_quotes:
                is_block_comment = not is_block_comment

            buffer = line.replace(
                TRIPLE_QUOTES[0], "\n").replace(
                TRIPLE_QUOTES[1], "\n")

            if not is_block_comment:
                buffer = buffer[2:]

            # Wrap this sub-paragraph as a markdown cell if
            # next line is end of code OR
            # (next line is a code but not a block comment) OR
            # (next line is nothing but not a block comment)
            if is_end_of_code or (
                next_is_code and not is_block_comment) or (
                    next_is_nothing and not is_block_comment
            ):
                arr.append("{}".format(buffer))
                markdown["source"] = arr
                cells.append(dict(markdown))
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
                code["source"] = arr
                cells.append(dict(code))
                arr = []
                is_running_code = False
            else:
                buffer = buffer + "\n"

                # Put another newline character if in a function
                try:
                    if data[i+1] == "" and (data[i+2].startswith("    #") or data[i+2].startswith("        #") or data[i+2].startswith("            #")):
                        buffer = buffer + "\n"
                except IndexError:
                    pass

                arr.append("{}".format(buffer))
                is_running_code = True
                continue

    # Finalise the contents of notebook
    final["cells"] = cells
    final.update(misc)

    # Write JSON to target file
    with open(target_filename, 'w') as outfile:
        json.dump(final, outfile)
        print("Notebook {} written.".format(target_filename))


def j2p_(source_filename, target_filename, overwrite, with_markdown=False):

    # Check if source file exists and read
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
        print("File {} exists. Add -o flag to overwrite this file,".format(target_filename) +
              " or specify a different name.")
        sys.exit(1)

    final = [cell["source"][0].replace("\n","\n# ")
             if cell["cell_type"] == "markdown" and with_markdown else cell["source"][0]
             for cell in myfile['cells']
             ]
    final = '\n\n'.join(final)

    with open(target_filename, "a") as outfile:
        outfile.write(final)


def main():

    # Get source and target filenames
    parser = argparse.ArgumentParser(
        description='Convert a Python script to Jupyter notebook')
    parser.add_argument('-r',
                        '--reverse',
                        action='store_true',
                        help="To convert Jupyter to Python script")
    parser.add_argument('-m',
                        '--markdown',
                        action='store_true',
                        help="To convert Jupyter to Python script with markdown")
    parser.add_argument('source_filename',
                        help='Python script to parse')
    parser.add_argument('-t',
                        '--target_filename',
                        help="""Target filename of Jupyter notebook. If not specified, it will use the filename of the Python script and append .ipynb""")
    parser.add_argument('-o',
                        '--overwrite',
                        action='store_true',
                        help='Flag whether to overwrite existing target file. Defaults to false')
    args = parser.parse_args()

    if args.reverse:
        j2p_(args.markdown, args.source_filename, args.target_filename, args.overwrite)
    else:
        p2j_(args.source_filename, args.target_filename, args.overwrite)


if __name__ == "__main__":
    main()
