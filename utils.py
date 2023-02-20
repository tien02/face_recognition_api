import os
import glob
import config
from PIL import Image

def remove_representation():
    '''
    Delete all representation_*.pkl in database after execute DeepFace verify
    '''
    representations_path = glob.glob(os.path.join(config.DB_PATH, "representations_*.pkl"))
    if len(representations_path) != 0:
        for representation in representations_path:
            if os.path.exists(representation):
                os.remove(representation)

def show_img(input_path:str):
    '''
    Read image from path and show
    
    Arguments:
        input_path (str) Path to the input image.
    '''

    if not isinstance(input_path, str):
        raise TypeError("Only string is accepted, expect an input path as string.")
    
    if not os.path.exists(input_path):
        raise ValueError('Path to the image is not available.')

    try:
        image = Image.open(input_path)
        image.show()
    except:
        print("Error when reading image, check input_path.")