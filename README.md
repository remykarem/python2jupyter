# py2nb (Beta)

Converts Python source code to Jupyter notebook.

The purpose of this repo is so that we can run a code paragraph-by-paragraph and don't have to do that by copying each paragraph of the code into every cell. It's also useful if we want to run our code in Google Colab.

This parser isn't perfect, but you would be satisfactorily pleased with what you get.

## Running

```bash
python your_python_file.py
```

and you will get a `notebook.ipynb` Jupyter notebook.

The `example.py` is a Keras tutorial on building an autoencoder for the MNIST dataset, found [here](https://github.com/keras-team/keras/blob/master/examples/mnist_denoising_autoencoder.py). You can run the example here:

```bash
python example.py
```

## Tests

Tested on macOS 10.14.

## How it works

Jupyter notebooks are just JSON files. The `py2nb.py` reads the source code line-by-line and determines whether it should be a markdown cell or a code cell, using a rule-based method.

## Project Structure

```txt
├── example.py              Example code
├── py2nb.py                The code that parses and generates the notebook
└── templates               JSON files that make up the final Jupyter notebook
    ├── cell_code.json
    ├── cell_markdown.json
    └── metadata.json
```

## Code format

The parser assumes a format where your code is paragraphed. Each paragraph has the comments part and/or the code part. The comments will be automatically converted to a markdown cell while the code will be, you guessed it, the code cell.

Some examples of well-documented code:

- [PyTorch Tutorials](https://pytorch.org/tutorials/beginner/pytorch_with_examples.html)
- [Keras Examples](https://github.com/keras-team/keras/tree/master/examples)
- [Scikit Learn Example](https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html#sphx-glr-auto-examples-classification-plot-digits-classification-py)