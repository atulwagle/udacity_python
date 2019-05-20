# Imports here

import torch
from torch import nn
from torch import optim
from torchvision import datasets, transforms

# Imports from user defined functions
from arg_parser import get_input_args_for_training
from handle_checkpoints import save_checkpoint
from model import create_model_instance

def train():

    # create argument parser
    in_arg = get_input_args_for_training()

    # parse the arguments and display them.
    data_directory, model_name, epochs, save_checkpoint_dir, learning_rate, hidden_units, gpu_mode = process_arguments(in_arg)

    # read from data directory and create loader
    dataloaders = load_data(data_directory)

    # based on the inputs create appropriate model, optimizer etc.
    model, optimizer, criterion = create_model(model_name, learning_rate, hidden_units, gpu_mode)

    # train the model and print validation loss etc.
    train_print_output(model, model_name, optimizer, criterion, gpu_mode, epochs, dataloaders, save_checkpoint_dir)

    return


def train_print_output(model, model_name, optimizer, criterion, gpu_mode, epochs, dataloaders, save_checkpoint_dir):
    print("Start training model ....")
    running_loss = 0
    device = gpu_mode
    for epoch in range(epochs):
        for inputs, labels in dataloaders['train']:

            # Move input and label tensors to the default device
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()

            logps = model.forward(inputs)
            loss = criterion(logps, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            
        else:
            validation_loss = 0
            accuracy = 0
            model.eval()
            with torch.no_grad():
                for inputs, labels in dataloaders['validation']:
                    inputs, labels = inputs.to(device), labels.to(device)
                    logps = model.forward(inputs)
                    batch_loss = criterion(logps, labels)

                    validation_loss += batch_loss.item()

                    # Calculate accuracy
                    ps = torch.exp(logps)
                    top_p, top_class = ps.topk(1, dim=1)
                    equals = top_class == labels.view(*top_class.shape)
                    accuracy += torch.mean(equals.type(torch.FloatTensor)).item()

            print(f"Epoch {epoch + 1}/{epochs}.. "
                  f"Train loss: {running_loss / len(dataloaders['train']):.3f}.. "
                  f"Validation loss: {validation_loss / len(dataloaders['validation']):.3f}.. "
                  f"Validation accuracy: {accuracy / len(dataloaders['validation']):.3f}")

            model.class_to_idx = dataloaders['train'].dataset.class_to_idx
                      
            running_loss = 0
            model.train()
            
    if save_checkpoint_dir is not None:
        save_checkpoint(save_checkpoint_dir, model, model_name, epoch, optimizer, running_loss)
        print("Saved checkpoint for model: ", model_name)
    else:
        print("Not saving the checkpoint.")
        print("End training model ....")
 
    return

def create_model(model_name, learning_rate, hidden_units, gpu_mode):
    device = gpu_mode

    model = create_model_instance(model_name)

    # Freeze parameters so we don't backprop through them
    for param in model.parameters():
        param.requires_grad = False

    dropout_rate = 0.2

    model.classifier = nn.Sequential(nn.Linear(25088, hidden_units),
                                     nn.ReLU(),
                                     nn.Dropout(dropout_rate),
                                     nn.Linear(hidden_units, 256),
                                     nn.ReLU(),
                                     nn.Dropout(dropout_rate),
                                     nn.Linear(256, 102),
                                     nn.LogSoftmax(dim=1))

    criterion = nn.NLLLoss()

    # Only train the classifier parameters, feature parameters are frozen
    optimizer = optim.Adam(model.classifier.parameters(), lr=learning_rate)

    model.to(device);

    return model, optimizer, criterion


def load_data(data_directory):
    train_dir = data_directory + '/train'
    valid_dir = data_directory + '/valid'

    train_transforms = transforms.Compose([transforms.RandomRotation(30),
                                           transforms.RandomResizedCrop(224),
                                           transforms.RandomHorizontalFlip(),
                                           transforms.ToTensor(),
                                           transforms.Normalize([0.485, 0.456, 0.406],
                                                                [0.229, 0.224, 0.225])])

    validation_transforms = transforms.Compose([transforms.Resize(255),
                                                transforms.CenterCrop(224),
                                                transforms.ToTensor(),
                                                transforms.Normalize([0.485, 0.456, 0.406],
                                                                     [0.229, 0.224, 0.225])])

    data_transforms = {'train': train_transforms, 'validation': validation_transforms}

    train_data = datasets.ImageFolder(train_dir, transform=data_transforms['train'])
    validation_data = datasets.ImageFolder(valid_dir, transform=data_transforms['validation'])

    image_datasets = {'train': train_data, 'validation': validation_data}

    trainloader = torch.utils.data.DataLoader(image_datasets['train'], batch_size=64, shuffle=True)
    validationloader = torch.utils.data.DataLoader(image_datasets['validation'], batch_size=64)

    dataloaders = {'train': trainloader, 'validation': validationloader}

    return dataloaders


def process_arguments(in_arg):
    data_directory = in_arg.data_dir
    model_name = in_arg.arch
    epochs = in_arg.epochs
    save_checkpoint_dir = in_arg.save_dir
    learning_rate = in_arg.learning_rate
    hidden_units = in_arg.hidden_units
    
    cuda_available = "cuda" if torch.cuda.is_available() else "cpu"
    gpu_mode = "cuda" if (in_arg.gpu == True and cuda_available == 'cuda') else "cpu"
    
    print ("\nInput arguments used for training the model:")
    print ("=============================================")
    print ("Location of data directory: ", data_directory)
    print ("Model Used: ", model_name)
    print ("Number of Epochs: ", epochs)
    print ("Location to save checkpoint: ", save_checkpoint_dir)
    print ("Learning Rate: ", learning_rate)
    print ("Hidden Units: ", hidden_units)
    print ("Mode model will be run: ", gpu_mode)
    print ("\n")
        
    return data_directory, model_name, epochs, save_checkpoint_dir, learning_rate, hidden_units, gpu_mode


# Call to main function to run the program
if __name__ == "__main__":
    train()
