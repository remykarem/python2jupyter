# p2j - Python to Jupyter Notebook

Convert your Python source code to Jupyter notebook with zero intervention.

The purpose of this package is to be able to run a code on Jupyter notebook without having to copy each paragraph of the code into every cell. It's also useful if we want to run our code in Google Colab.

In a nutshell, every paragraph of your code is transformed into a code cell.

This parser isn't perfect, but you would be satisfactorily pleased with what you get.

See an example of a [Python source code](p2j/examples/example3.py) and its [Jupyter notebook](p2j/examples/example3.ipynb) after converting.

## Installing

```bash
pip install p2j
```

## Running

```bash
p2j code_to_parse.py
```

and you will get a `code_to_parse.ipynb` Jupyter notebook. See `p2j -h` for other arguments.

To run examples from this repository, first clone this repo

```bash
git clone https://github.com/raibosome/python2jupyter.git
```

and after you `cd` into the project, run

```bash
p2j examples/example.py
```

The `examples/example.py` is a Keras tutorial on building an autoencoder for the MNIST dataset, found [here](https://github.com/keras-team/keras/blob/master/examples/mnist_denoising_autoencoder.py).

## Tests

Tested on macOS 10.14 with Python 3.6.

## How it works

Jupyter notebooks are just JSON files. The `py2nb.py` reads the source code line-by-line and determines whether it should be a markdown cell or a code cell, using a rule-based method. It also respects the following:

- Blocks of indented code. Comments from within are kept as a code cell. Eg. classes, function definitions and loops
- Docstrings
- Pylint directives are converted to code cells

## Project Structure

```txt
├── p2j             The parser module
│   ├── __init__.py
│   ├── examples    Example codes that you can parse
│   ├── p2j.py      Main file
│   └── templates   JSON files needed to build the notebook
├── README.md       This file
├── LICENSE         Licensing
├── MANIFEST.in     Python packaging-related
├── build           Python packaging-related
├── dist            Python packaging-related
├── p2j.egg-info    Python packaging-related
└── setup.py        Python packaging-related
```

## Code format

There is no specific format that you should follow, but generally the parser assumes a format where your code is paragraphed. Each paragraph has the comments part and/or the code part. The comments will be automatically converted to a markdown cell while the code will be, you guessed it, the code cell.

Some examples of well-documented code (and from which you can test!):

- [PyTorch Tutorials](https://pytorch.org/tutorials/beginner/pytorch_with_examples.html)
- [Keras Examples](https://github.com/keras-team/keras/tree/master/examples)
- [Scikit Learn Example](https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html#sphx-glr-auto-examples-classification-plot-digits-classification-py)

## Pull requests

Pull requests are very much encouraged!
