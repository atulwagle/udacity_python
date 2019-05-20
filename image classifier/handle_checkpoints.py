import torch
import os

# Imports from user defined functions
from model import create_model_instance

##
## This file handles saving and loading of checkpoints for a given model.
##
def save_checkpoint(save_checkpoint_dir, model, model_name, epoch, optimizer, running_loss):
    """
    Save the model with it's associated parameters.
    File will be saved under the directory provided and model name will be the check point filename.
    """
    checkpoint = {
        'epoch': epoch,
        'model_dict': model.state_dict(),
        'model_classifier': model.classifier,
        'optimizer_dict': optimizer.state_dict(),
        'class_to_idx': model.class_to_idx,
        'running_loss': running_loss
    }
    torch.save(checkpoint, os.path.join(save_checkpoint_dir, model_name + '.ckpt'))
    return


def load_from_checkpoint(checkpoint_path, model_name):
    """
    Load a checkpoint for a given model.
    """
    model = create_model_instance(model_name)
    
    checkpoint = torch.load(checkpoint_path)
    model.class_to_idx = checkpoint['class_to_idx']
    model.classifier = checkpoint['model_classifier']
    model.load_state_dict(checkpoint['model_dict'])
    optimizer = checkpoint['optimizer_dict']
    epoch = checkpoint['epoch']
    running_loss = checkpoint['running_loss']
    
    return model, optimizer, epoch, running_loss
