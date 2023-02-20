import os 
import config
from PIL import Image
from deepface import DeepFace
from utils import remove_representation

def faceRecognition(query_img_path:str) -> str:
    '''
    Do Face Recognition task, give the image which is 
    the most similar with the input image from the 
    database - in this case is a folder of images

    Argument:
        query_img_path (str) Path to the query image
    Return:
        value_img_path (str) Path to the value image
    '''

    if not isinstance(query_img_path, str):
        raise TypeError("Only string is accepted, expect a query image path as string.")
    
    if not os.path.exists(query_img_path):
        raise ValueError('Path to the image is not available.')
    
    df = DeepFace.find(img_path=query_img_path, 
                        db_path=config.DB_PATH, 
                        model_name=config.MODELS[config.MODEL_ID], 
                        distance_metric=config.METRICS[config.METRIC_ID], 
                        detector_backend=config.DETECTORS[config.DETECTOR_ID], 
                        silent=True)
    
    if not df.empty:
        path_to_img, metric = df.columns
        df = df.sort_values(by=[metric], ascending=False)
        value_img_path = df[path_to_img].iloc[0]
        # for test
        # remove_representation()

        return value_img_path
    else:
        print("No image found")
        return []

def faceRegister(input_path:str, img_name:str):
    '''
    Add new user to the database for Face Recognition task 
    by registering. Resize image if necessary.

    Arguments:
        input_path (str) Path to the input image.
        img_name (str) Image's name, expect to be unique in the database.
    '''
    if not isinstance(input_path, str):
        raise TypeError("Only string is accepted, expect an input path as string.")
    
    if not os.path.exists(input_path):
        raise ValueError('Path to the image is not available.')

    save_img_path = img_name + ".jpg"
    if os.path.exists(os.path.join(config.DB_PATH,save_img_path)):
        raise ValueError(f"{save_img_path} already in the database.")
    
    try:
        image = Image.open(input_path)
        if config.RESIZE:
            image = image.resize(config.SIZE)

        image = image.save(os.path.join(config.DB_PATH, save_img_path))
        print(f"Image has already save at {os.path.join(config.DB_PATH, save_img_path)}")

        remove_representation()
        return True
    except:
        print("Error when reading image, check input_path.")
        return False

def changeImageName(src_path:str, dst_path:str):
    '''
    Change Image Name in database

    Arguments:
        src_path (str) Path to the source name
        dst_path (str) Path to the destination name
    '''
    if not isinstance(src_path, str):
        raise TypeError("Only string is accepted, expect a source path as string.")
    if not isinstance(dst_path, str):
        raise TypeError("Only string is accepted, expect a destination path as string.")
    
    if not os.path.exists(src_path):
        raise ValueError('Path to the image is not available.')
    if os.path.exists(dst_path):
        raise ValueError(f"{dst_path} already in the database.")

    os.rename(src_path, dst_path)

    if os.path.exists(dst_path):
        print(f"Already change image to {dst_path}")
        return True
    else:
        print("Some error happened!")
        return False

def deleteImage(img_path:str):
    if not isinstance(img_path, str):
        raise TypeError("Only string is accepted, expect a image path as string.")
    
    if not os.path.exists(img_path):
        raise ValueError('Path to the image is not available.')
    
    os.remove(img_path)

    if not os.path.exists(img_path):
        print(f"{img_path} has been deleted.")
        return True
    else:
        print("Some error happend")
        return False