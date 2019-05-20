# Imports python modules
import argparse

##
## This file handles the input arguments used for training and predicting the models.
##
def get_input_args_for_training():
    """
    Retrieves and parses command line arguments provided by the user when
    they run the program from a terminal window.
    Command Line Arguments:
      1. CNN Model Architecture as --arch with default value 'vgg'.
         Supporting two models VGG13 and VGG16.
      2. Directory to save the checkpoint.
      3. Learning Rate for the model.
      4. Nodes to be created for the model for the hidden layer.
      5. Number of epochs to used to train the model.
      6. Enable GPU mode for the model

    This function returns these arguments as an ArgumentParser object.
    Parameters:
        None - simply using argparse module to create & store command line arguments
    Returns:
        parse_args() -data structure that stores the command line arguments object
    """

    # Create Parse using ArgumentParser
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str,
                        help='Directory of data')
    parser.add_argument('--arch', type=str, default='vgg16', choices=['vgg13', 'vgg16'],
                        help='Name of CNN Model Architecture')
    parser.add_argument('--save_dir', type=str,
                        help='Directory to save Checkpoint')
    parser.add_argument('--learning_rate', type=float, default=0.001,
                        help='Learning Rate')
    parser.add_argument('--hidden_units', type=int, default=1024,
                        help='Hidden Layers')
    parser.add_argument('--epochs', type=int, default=10,
                        help='Epochs to train the model')
    parser.add_argument('--gpu', default="cpu", action="store_true",
                        help='Enable GPU Mode')

    return parser.parse_args()

def get_input_args_for_prediction():
    """
    Retrieves and parses command line arguments provided by the user when
    they run the program from a terminal window.
    Command Line Arguments:
      1. Directory of the image to be tested.
      2. Directory of the checkpoint.
      3. Top-K probablities.
      4. Category output label names.
      5. Enable GPU mode for the model.

    This function returns these arguments as an ArgumentParser object.
    Parameters:
        None - simply using argparse module to create & store command line arguments
    Returns:
        parse_args() -data structure that stores the command line arguments object
    """
    # Create Parse using ArgumentParser
    parser = argparse.ArgumentParser()
    parser.add_argument('image_dir', type=str,
                        help='Directory of the image')
    parser.add_argument('checkpoint_dir', type=str,
                        help='Directory of saved checkpoint')
    parser.add_argument('--top_k', type=int, default='5',
                        help='Number of top k classes/probablities')
    parser.add_argument('--category_names', type=str, default='./cat_to_name.json',
                        help='Location of the category file')
    parser.add_argument('--gpu', default="cpu", action="store_true",
                        help='Enable GPU Mode')

    return parser.parse_args()
