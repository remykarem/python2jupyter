"""
This code translate .py files to .ipynb
"""
# We only need the json package
import json
import requests

# Reserved Python keywords
RESERVED = ['for', 'with', 'class', 'while']

# Read source file
with open('examples/example3.py', 'r') as file:
    data = [l.rstrip('\n') for l in file]

# url = 'https://raw.githubusercontent.com/keras-team/keras/master/examples/mnist_denoising_autoencoder.py'
# data = requests.get(url).text
# print(data)

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
with open('example.ipynb', 'w') as outfile:
    json.dump(final, outfile)
