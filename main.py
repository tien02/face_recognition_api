import os 
import config
from PIL import Image
from deepface import DeepFace
from utils import remove_representation
from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Welcome to Face Recognition API!"
    }

@app.get("/face-recognition")
async def face_recognition(query_img_path:str=Query(..., description="Path to the query image file")) -> str:

    '''
    Do Face Recognition task, give the image which is 
    the most similar with the input image from the 
    database - in this case is a folder of images

    Argument:
        query_img_path (str) Path to the query image (e.g: images/img1.jpeg)
    Return:
        value_img_path (str) Path to the value image
    '''
    
    if not os.path.exists(query_img_path):
        raise HTTPException(status_code=404, detail='Path to the image is not exist!')
    
    df = DeepFace.find(img_path=query_img_path, 
                        db_path=config.DB_PATH, 
                        model_name=config.MODELS[config.MODEL_ID], 
                        distance_metric=config.METRICS[config.METRIC_ID], 
                        detector_backend=config.DETECTORS[config.DETECTOR_ID], 
                        silent=True)
    
    if not df.empty:
        path_to_img, metric = df.columns
        ascending = True
        if config.METRIC_ID == 0:
            ascending = False
        df = df.sort_values(by=[metric], ascending=ascending)
        value_img_path = df[path_to_img].iloc[0]

        return value_img_path
    else:
        return "No Image Found"

@app.post('/face_register')
async def face_register(input_path:str = Query(..., description="Path to input image"), img_name: str=Query(..., description="Image name")):
    '''
    Add new user to the database for Face Recognition task 
    by registering. Resize image if necessary.

    Arguments:
        input_path (str) Path to the input image. (e.g: images/img1.jpeg)
        img_name (str) Image's name, expect to be unique in the database. (e.g: im2)
    '''
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail='Path to the image is not exist!')

    save_img_path = img_name
    if "." not in img_name:
        extension = input_path.split(".")[1]
        save_img_path = save_img_path + "." + extension
    save_img_path = os.path.join(config.DB_PATH,save_img_path)
    if os.path.exists(save_img_path):
        raise HTTPException(status_code=409, detail=f"{save_img_path} already in the database.")
    
    image = Image.open(input_path)
    if config.RESIZE:
        image = image.resize(config.SIZE)

    image = image.save(save_img_path)
    remove_representation() # delete all representation_*.pkl created by DeepFace.find
    return {
        "message": f"Image has been saved at {save_img_path}"
        }
    

@app.put('/change-image-name')
async def change_img_name(src_path:str = Query(..., description="File image going to be change"), img_name:str = Query(..., description="New name")):
    '''
    Change file name in database

    Arguments:
        src_path (str) Path to the source name (e.g: images/img1.jpeg)
        img_name (str) Name to be change (e.g: im2)
    Returns:
        images/img1.jpeg -> images/im2.jpeg
    '''
    new_path = src_path.split("/")[:-1] + img_name
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

@app.delete('/delete')
async def del_img(img_path:str = Query(..., description="Path to the image need to be deleted")):
    '''
    Delete Image from image path

    Arguments:
        img_path (str) Path to the image (e.g: images/img1.jpeg)
    '''
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail=f'Path to {img_path} is not exist!')
    
    os.remove(img_path)

    return {
        "message": f"{img_path} has already been deleted"
    }