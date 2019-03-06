"""
This is mostly just the tutorial from
https://pytorch.org/tutorials/beginner/nlp/sequence_models_tutorial.html
with the following changes:

 1. read data from files
 2. separate test data and validation data
 3. add tqdm with loss metrics
 4. early stopping based on validation loss
 5. track accuracy during training / validation
"""

# pylint: disable=invalid-name,redefined-outer-name
