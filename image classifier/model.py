from torchvision import models

##
## This file handles model creation.
##
def create_model_instance(model_name):
    """
    This function creates an instance of pretrained model.
    If an invalid input is given then the program exits with an error.
    :param model_name: Name of the model to be created. Supported ones are VGG13 and VGG16.
    :return: model
    """
    if model_name == "vgg13":
        model = models.vgg13(pretrained=True)
    elif model_name == "vgg16":
        model = models.vgg16(pretrained=True)
    else:
        print("**** Model is not supported. Model: ",
              model_name)
        exit(1)

    return model
