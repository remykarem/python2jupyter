import json

with open('example.py', 'r') as file:
    data = [l.rstrip('\n') for l in file]

with open('cell.json') as file:
    cell = json.load(file)
with open('markdown.json') as file:
    markdown = json.load(file)
with open('misc.json') as file:
    misc = json.load(file)

RESERVED = ['for', 'with', 'class', 'while']

final = {}
cells = []

end_paragraph = True
buffer = ""
arr = []
is_running_comment = False
is_running_code = False
next_is_code = False
next_is_nothing = False
next_is_comment = False
num_lines = len(data)
is_running_function = False
next_is_function = False

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
        next_is_function = data[i+1][:4] == "    " or (data[i+1] == "" and data[i+2][:4] == "    ")
        print(line)
        print(data[i+1][:4] == "")
    except:
        pass
    end_of_code = i == num_lines-1

    if line == "":
        continue

    # Sub-paragraph is a comment but not a running code
    if (is_running_comment or line[0] == "#") and not is_running_code:
        buffer = line[2:]
        # Close this if next line is code or next line is space or end of code
        if end_of_code or next_is_code or next_is_nothing:
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
    # Sub-paragraph is a comment but not a running code
    else:
        buffer = line
        # Close this if next line is end of code or next is nothing 
        # Don't close if next is still part of a
        if (end_of_code or next_is_nothing) and not (next_is_nothing and next_is_function):# or not next_is_function) or (not next_is_function and next_is_nothing):
            arr.append(f"{buffer}")
            cell["source"] = arr
            cells.append(dict(cell))
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

final["cells"] = cells
final.update(misc)

with open('mynb.json', 'w') as outfile:
    json.dump(final, outfile)

with open('mynb.ipynb', 'w') as outfile:
    json.dump(final, outfile)
