import os
import sys


def _check_files(source_file: str, target_file: str, overwrite: bool, conversion: str):
    """File path checking

    Check if
    1) Name of source file is valid.
    2) Target file already exists. If not, create.

    Does not check if source file exists. That will be done
    together when opening the file.
    """

    if conversion == "p2j":
        expected_src_file_ext = ".py"
        expected_tgt_file_ext = ".ipynb"
    else:
        expected_src_file_ext = ".ipynb"
        expected_tgt_file_ext = ".py"

    file_base = os.path.splitext(source_file)[0]
    file_ext = os.path.splitext(source_file)[-1]

    if file_ext != expected_src_file_ext:
        print("Wrong file type specified. Expected {} ".format(expected_src_file_ext) +
              "extension but got {} instead.".format(file_ext))
        sys.exit(1)

    # Check if target file is specified and exists. If not specified, create
    if target_file is None:
        target_file = file_base + expected_tgt_file_ext
    if not overwrite and os.path.isfile(target_file):
        # FileExistsError
        print("File {} exists. ".format(target_file) +
              "Add -o flag to overwrite this file, " +
              "or specify a different target filename using -t.")
        sys.exit(1)

    return target_file
