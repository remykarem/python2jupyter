import sys
import json
from p2j.utils import _check_files


def jupyter2python(source_filename: str, target_filename: str, overwrite: bool = False):
    """Convert Jupyter notebooks to Python scripts

    Args:
        source_filename (str): Path to Jupyter notebook.
        target_filename (str): Path to name of Python script. Optional.
        overwrite (bool): Whether to overwrite an existing Python script.
        with_markdown (bool, optional): Whether to include markdown. Defaults to False.
    """

    target_filename = _check_files(
        source_filename, target_filename, overwrite, conversion="j2p")

    # Check if source file exists and read
    try:
        with open(source_filename, "r", encoding="utf-8") as infile:
            myfile = json.load(infile)
    except FileNotFoundError:
        print("Source file not found. Specify a valid source file.")
        sys.exit(1)

    final = ["".join(["# " + line.lstrip() for line in cell["source"] if not line.strip() == ""])
             if cell["cell_type"] == "markdown" else "".join(cell["source"])
             for cell in myfile["cells"]]
    final = "\n\n".join(final)
    final = final.replace("<br>", "")

    with open(target_filename, "a", encoding="utf-8") as outfile:
        outfile.write(final)
        print("Python script {} written.".format(target_filename))
