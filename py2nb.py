"""
This code translate .py files to .ipynb
"""
# Standard imports for file handling and JSON files
import argparse
import os
import sys
import json

# Reserved Python keywords
RESERVED = ['for', 'with', 'class', 'while']

# Get source and target filenames
parser = argparse.ArgumentParser(description='Parse a file.')
parser.add_argument('source_filename', help='File to parse')
parser.add_argument('-t', '--target_filename', help='Target filename')
parser.add_argument('-o', '--overwrite', action='store_true', help='Flag to overwrite existing target file')
args = parser.parse_args()
source_filename = args.source_filename
target_filename = args.target_filename
overwrite = args.overwrite

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
    print("Target file not specified. Creating a default notebook with name {}.".format(target_filename))
if not overwrite and os.path.isfile(target_filename):
    print("File {} exists. Add -o flag to overwrite or specify a different name.".format(target_filename))
    sys.exit(1)

# Read JSON files for .ipynb template
with open('templates/cell_code.json') as file:
    code = json.load(file)
with open('templates/cell_markdown.json') as file:
    markdown = json.load(file)
with open('templates/metadata.json') as file:
    misc = json.load(file)

# Initialise variables
final = {}
cells = []
arr = []
num_lines = len(data)

# Initialise variables for checks
is_block_comment = False
end_paragraph = True
is_running_comment = False
is_running_code = False
next_is_code = False
next_is_nothing = False
next_is_comment = False
is_running_function = False
next_is_function = False

# Read source code line by line
for i, line in enumerate(data):

    buffer = ""

    # Check next line
    try:
        next_is_code = data[i+1][0] != "#"
    except:
        pass
    try:
        next_is_comment = data[i+1][0] == "#"
    except:
        pass
    try:
        next_is_nothing = data[i+1] == ""
    except:
        pass
    try:
        next_is_function = data[i+1][:4] == "    " or (
            data[i+1] == "" and data[i+2][:4] == "    ")
        # print(line)
        # print(data[i+1][:4] == "")
    except:
        pass
    end_of_code = i == num_lines-1

    # Skip if line is empty
    if line == "":
        continue

    # Sub-paragraph is a comment but not a running code
    if (is_running_comment or (line[0] == "#" and (line[:8] != "# pylint" or line[:7] != "#pylint")) or line[:3] == "'''" or line[-3:] == "'''" or line[:3] == "\"\"\"" or line[-3:] == "\"\"\"") and not is_running_code:

        if line[:3] == "'''" or line[-3:] == "'''" or line[:3] == "\"\"\"" or line[-3:] == "\"\"\"":
            is_block_comment = not is_block_comment
        
        if is_block_comment:
            buffer = line.replace("'''", "").replace("\"\"\"", "")
        else:
            buffer = line[2:]

        # Wrap this sub-paragraph as a cell
        # if next line is code or next line is space or end of code
        if end_of_code or (next_is_code and not is_block_comment) or (next_is_nothing and not is_block_comment):
            arr.append(f"{buffer}")
            markdown["source"] = arr
            cells.append(dict(markdown))
            arr = []
            is_running_comment = False
        else:
            buffer = buffer + "<br>"
            arr.append(f"{buffer}")
            is_running_comment = True
            continue
    else:  # Sub-paragraph is a comment but not a running code
        buffer = line

        # Close this if next line is end of code or next is nothing
        # Don't close if next is still part of a
        # or not next_is_function) or (not next_is_function and next_is_nothing):
        if (end_of_code or next_is_nothing) and not (next_is_nothing and next_is_function):
            arr.append(f"{buffer}")
            code["source"] = arr
            cells.append(dict(code))
            arr = []
            is_running_code = False
        else:
            buffer = buffer + "\n"

            # Put another newline character if in a function
            try:
                if data[i+1] == "" and (data[i+2][:5] == "    #" or data[i+2][:9] == "        #"):
                    buffer = buffer + "\n"
            except:
                pass

            arr.append(f"{buffer}")
            is_running_code = True
            continue

# Finalise the contents of notebook
final["cells"] = cells
final.update(misc)

# Write JSON to target file
with open(target_filename, 'w') as outfile:
    json.dump(final, outfile)
    print("Notebook {} written.".format(target_filename))
