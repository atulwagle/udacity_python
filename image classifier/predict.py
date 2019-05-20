# Imports here
import json
import torch
from torch import nn
from torch import optim

import numpy as np
import torch.nn.functional as F
from torchvision import datasets, transforms, models
from PIL import Image

# Imports from user defined functions
from handle_checkpoints import load_from_checkpoint
from arg_parser import get_input_args_for_prediction

def predict():
    ''' Predict the class (or classes) of an image using a trained deep learning model.
    '''
    
    # create argument parser
    in_arg = get_input_args_for_prediction()
    
    # parse the arguments and display them.
    image_dir, checkpoint_dir, top_k, category_names_dir, gpu_mode, model_name = process_arguments(in_arg)
    
    # Implement the code to predict the class from an image file
    processed_image = process_image(image_dir)
    processed_image_torch = torch.from_numpy(processed_image)
    processed_image_torch = processed_image_torch.type(torch.FloatTensor)
    processed_image_torch.unsqueeze_(0)
    
    model, optimizer, epoch, running_loss = load_from_checkpoint(checkpoint_dir, model_name)  
    model.train(False)
    model.eval()
    model.to("cpu")

    logps = model.forward(processed_image_torch)
    ps = torch.exp(logps)
    top_p, top_class = ps.topk(top_k, dim=1)
    
    top_p = top_p.detach().numpy().tolist()[0] 
    top_class = top_class.detach().numpy().tolist()[0]

    idx_to_class = {}
    for key, value in model.class_to_idx.items():
        idx_to_class [value] = key
            
    top_idxs = []
    for i in top_class:
        top_idxs.append(idx_to_class[i])

    # load category file
    cat_to_name = load_class_file(category_names_dir)

    # create list of top labels
    labels = []
    for index in top_idxs:
        labels.append(cat_to_name[index])

    for label, probability in zip(labels, top_p):
        print("Label: ", label)
        print("Probability: ", int(probability * 100), "%")

    return top_p, labels

def process_image(image_dir):
    ''' Scales, crops, and normalizes a PIL image for a PyTorch model,
        returns an Numpy array
    '''
    
    # Process a PIL image for use in a PyTorch model
    
    pil_image = Image.open(image_dir)
    width, height = pil_image.size
    aspect_ratio = width/height
    
    if (width<256):
        updated_height = 256/aspect_ratio
        pil_image = pil_image.resize((256, updated_height), resample=0)
    elif (height<256):
        updated_width = 256/aspect_ratio
        pil_image = pil_image.resize((updated_width, 256), resample=0)

    resized_width, resized_height = pil_image.size
    left_margin = (resized_width-224)/2
    bottom_margin = (resized_height-224)/2
    right_margin = left_margin + 224
    top_margin = bottom_margin + 224
    
    pil_image = pil_image.crop((left_margin, bottom_margin, right_margin, top_margin))
    np_image = np.array(pil_image)
    np_image = np.array(np_image)/255

    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    
    np_image = (np_image - mean)/std
    return np_image.transpose(2, 0, 1)

def load_class_file(file_name):
    """
    Load the category labels file.
    """
    with open(file_name, 'r') as f:
        cat_to_name = json.load(f)
        
    return cat_to_name
    
def process_arguments(in_arg):
    """
    Parse through the input arguments and assign them to variables.
    """
    image_dir = in_arg.image_dir
    checkpoint_dir = in_arg.checkpoint_dir
    top_k = in_arg.top_k
    category_names_dir = in_arg.category_names
    cuda_available = "cuda" if torch.cuda.is_available() else "cpu"
    gpu_mode = "cuda" if (in_arg.gpu == True and cuda_available == 'cuda') else "cpu"    
    
    model_name = ''
    
    for i in in_arg.checkpoint_dir.split('/'):
        if i.find('ckpt') > 0:
            x = i.split('.')
            model_name=x[0]
            
    print ("\nInput arguments used for predicting the image:")
    print ("===============================================")
    print ("Location of image file: ", image_dir)
    print ("Location of checkpoint file: ", checkpoint_dir)
    print ("Top-K: ", top_k)
    print ("Location of category file: ", category_names_dir)
    print ("Mode model will be run: ", gpu_mode)
    print ("Model name: ", model_name)
    print ("\n")

    return image_dir, checkpoint_dir, top_k, category_names_dir, gpu_mode, model_name

# Call to main function to run the program
if __name__ == "__main__":
    predict()
