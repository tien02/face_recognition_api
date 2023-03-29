import os 
import glob
import shutil
import app.config as config
import cv2 as cv
from PIL import Image
from deepface import DeepFace
from app.utils import remove_representation, check_empty_db

from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query, HTTPException, File, UploadFile

import numpy as np

app = FastAPI()

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    '''
    Greeting!!!
    '''
    if os.path.exists(config.DB_PATH):
        return {
            "message": "Welcome to Face Recognition API."
        }
    else:
        return {
            "message": f"Error when trying to connect {config.DB_PATH}, there is no database available."
        }


@app.get('/img-db-info')
def get_img_db_info(return_img_file:bool | None = True):
    '''
    Get database information, return all files in the database
    '''
    numer_of_images = len(os.listdir(config.DB_PATH))
    pkl_pattern = glob.glob(os.path.join(config.DB_PATH, '*.pkl'))
    pkl_pattern = [file.split('/')[-1] for file in pkl_pattern]

    hidden_pattern = glob.glob(os.path.join(config.DB_PATH, ".*"))
    hidden_pattern = [file.split('/')[-1] for file in hidden_pattern]
    
    unshow_file = pkl_pattern + hidden_pattern

    if len(pkl_pattern) != 0:
        numer_of_images -= len(unshow_file)
    
    if return_img_file:
        return {
            "number_of_image": numer_of_images,
            "all_images_file": [file for file in os.listdir(config.DB_PATH) if file not in unshow_file],
        }
    else:
        return {
            "number_of_image": numer_of_images,
        }


@app.get('/show_img/{img_path}')
def show_img(img_path: str | None = None):
    '''
    Return image file from given image name

    Arguments:  
        img_path(str): image file
        return_image_name(bool): Decide whether return only image file (img) or image file with extension (img.[jpg|jpeg])
    '''
    empty = empty = check_empty_db()
    if empty:
        return "No image found in the database"
    
    if img_path is None:
        return {
            "error": "Client should provide image file name"
        }
    
    img_pattern = glob.glob(os.path.join(config.DB_PATH, "*" + img_path + "*"))
    return FileResponse(img_pattern[0])


@app.post('/register')
def face_register(
    img_file: UploadFile | None = File(None, description="Upload Image"),
    to_gray: bool | None = Query(
            default=True, 
            description="Whether save image in gray scale or not"),
    img_save_name: str | None = Query(
        default=None,
        description="File's name to be save, file extension can be available or not",
    ),):
    '''
    Add new user to the database by face registering. Resize image if necessary.

     Arguments:  
        img_file(File): upload image file
        img_save_name(string): name of image file need to be saved
    '''

    if img_file is None:
        return {
            "message": "Image file need to be sent!",
        }

    save_img_dir = ''
    if img_save_name is not None:

        extension = img_file.filename.split(".")[-1]
        if "." in img_save_name:
            img_save_name_extension = img_save_name.split(".")[-1]
            if extension != img_save_name_extension:
                raise HTTPException(status_code=404, detail='File extension should match')
            save_img_dir = os.path.join(config.DB_PATH, img_save_name)

        else:
            save_img_dir = os.path.join(config.DB_PATH, img_save_name + "." + extension)
        
    
    else:
        save_img_dir = os.path.join(config.DB_PATH, img_file.filename)
    
    if os.path.exists(save_img_dir):
        raise HTTPException(status_code=409, detail=f"{save_img_dir} has already in the database.")
    
    if (config.RESIZE is False) and (to_gray is False):
        with open(save_img_dir, "wb") as w:
            shutil.copyfileobj(img_file.file, w)

    else:
        try:
            image = Image.open(img_file.file)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            
            if config.RESIZE:
                image = image.resize(config.SIZE)

            np_image = np.array(image)
            np_image = cv.cvtColor(np_image, cv.COLOR_RGB2BGR)

            if to_gray:
                np_image = cv.cvtColor(np_image, cv.COLOR_BGR2GRAY)

            cv.imwrite(save_img_dir, np_image)
        except:
            raise HTTPException(status_code=500, detail="Something went wrong when saving the image")
        finally:
            img_file.file.close()
            image.close()
        

    remove_representation() # delete all representation_*.pkl created by DeepFace.find
    return {
        "message": f"{img_file.filename} has been save at {save_img_dir}.",
    }


@app.post("/recognition/")
def face_recognition(
    img_file:UploadFile =  File(...,description="Query image file"),
    to_gray: bool | None = Query(
            default=True, 
            description="Whether save image in gray scale or not"),
    return_image_name:bool = Query(default=True, description="Whether return only image name or full image path"),
):

    '''
    Do Face Recognition task, give the image which is 
    the most similar with the input image from the 
    database - in this case is a folder of images

    Arguments:  
        img_file(File): image file
        return_image_name(bool): Decide whether return only image file (img) or image file with extension (img.[jpg|jpeg])
    Return:
        Return path to the most similar image file
    '''

    empty = check_empty_db()
    if empty:
        return "No image found in the database"

    if len(os.listdir(config.DB_PATH)) == 0:
        return {
            "message": "No image found in the database."
        }
    
    if not os.path.exists("query"):
        os.makedirs("query")

    query_img_path = os.path.join("query", img_file.filename)

    if to_gray:
        image = Image.open(img_file.file)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        np_image = np.array(image)
        np_image = cv.cvtColor(np_image, cv.COLOR_BGR2GRAY)

        cv.imwrite(query_img_path, np_image)
    else:
        with open(query_img_path, "wb") as w:
            shutil.copyfileobj(img_file.file, w)

    # try:
    df = DeepFace.find(img_path=query_img_path, 
                        db_path = config.DB_PATH, 
                        model_name = config.MODELS[config.MODEL_ID], 
                        distance_metric = config.METRICS[config.METRIC_ID], 
                        detector_backend = config.DETECTORS[config.DETECTOR_ID], 
                        silent = True, align = True, prog_bar = False, enforce_detection=False)
    # except:
    #     return {
    #         'error': "Error happening when trying to detecting face or reconition"
    #     }
    
    os.remove(query_img_path)

    if not df.empty:
        path_to_img, metric = df.columns
        ascending = True
        if config.METRIC_ID == 0:
            ascending = False
        df = df.sort_values(by=[metric], ascending=ascending)
        value_img_path = df[path_to_img].iloc[0]

        if return_image_name:
            return_value = value_img_path.split(os.path.sep)[-1]
            return_value = return_value.split(".")[0]
            return {
                "result": return_value,
            }
        else:
            return {
                "result": value_img_path,
            }
    else:
        return {
            "result": "No faces have been found"
        }


@app.put('/change-file-name')
def change_img_name(
    src_path:str = Query(..., description="File image going to be change"), 
    img_name:str = Query(..., description="New name")
    ):
    '''
    Change file name in database

    Arguments:
        src_path (str) Path to the source name (e.g: images/img1.jpeg)
        img_name (str) Name to be change (e.g: im2)
    Returns:
        images/img1.jpeg -> images/im2.jpeg
    '''

    empty = empty = check_empty_db()
    if empty:
        return "No image found in the database"

    src_path = os.path.join(config.DB_PATH, src_path)
    
    new_path = "/".join(src_path.split("/")[:-1]) + "/" + img_name
    if "." not in img_name:
        extension = src_path.split(".")[1]
        new_path = new_path + "." + extension

    if not os.path.exists(src_path):
        raise HTTPException(status_code=404, detail=f'Path to {src_path} is not exist!')

    if os.path.exists(new_path):
        raise HTTPException(status_code=409, detail=f"{new_path} already in the database.")

    os.rename(src_path, new_path)

    return {
        "message": f"Already change {src_path} file name to {new_path}"
    }


@app.delete('/del-single-image')
def del_img(img_path:str = Query(..., description="Path to the image need to be deleted")):
    '''
    Delete single image file in database

    Arguments:
        img_path (str) Path to the image (e.g: images/img1.jpeg)
    '''
    empty = check_empty_db()
    if empty:
        return "No image found in the database"

    img_path = os.path.join(config.DB_PATH, img_path)

    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail=f'Path to {img_path} is not exist!')
    
    os.remove(img_path)

    return {
        "message": f"{img_path} has already been deleted!"
    }


@app.delete('/reset-db')
def del_db():
    '''
    Delete all file in database ~ Delete database
    '''
    empty = check_empty_db()
    if empty:
        return "No image found in the database"

    
    for file in os.listdir(config.DB_PATH):
        os.remove(os.path.join(config.DB_PATH, file))
    
    if len(os.listdir(config.DB_PATH)) == 0:
        return {
            "message": "All file have been deleted!"
        }
    else:
        raise HTTPException(status_code=500, detail="Some thing wrong happened.")