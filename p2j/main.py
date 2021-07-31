import argparse
from p2j.p2j import python2jupyter
from p2j.j2p import jupyter2python


def main():

    parser = argparse.ArgumentParser(
        description="Convert a Python script to Jupyter notebook and vice versa",
        usage="p2j myfile.py")
    parser.add_argument("source_filename",
                        help="Python script to parse")
    parser.add_argument("-r", "--reverse",
                        action="store_true",
                        help="To convert Jupyter to Python scripto")
    parser.add_argument("-t", "--target_filename",
                        help="Target filename of Jupyter notebook. If not specified, " +
                        "it will use the filename of the Python script and append .ipynb")
    parser.add_argument("-o", "--overwrite",
                        action="store_true",
                        help="Flag whether to overwrite existing target file.")
    args = parser.parse_args()

    if args.reverse:
        python2jupyter(source_filename=args.source_filename,
                       target_filename=args.target_filename,
                       overwrite=args.overwrite)
    else:
        jupyter2python(source_filename=args.source_filename,
                       target_filename=args.target_filename,
                       overwrite=args.overwrite)


if __name__ == "__main__":
    main()
