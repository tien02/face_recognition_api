# Face Recognition API

## Tools
* Face Recognition model: [deepface](https://github.com/serengil/deepface)

* API: [fastapi](https://github.com/tiangolo/fastapi)

## Directory structure
Expects project's directory structure as:
```
├── project
│   ├── app
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── utils.py
|   |
│   ├── img_db  # Database - Folder of images
│   │   ├── *.[jpg | jpeg]
|   |
│   ├── images  # Query - Folder of images need to find id
│   │   ├── *.[jpg | jpeg]
|   |
|   ├── Dockerfile
|   ├── docker_build.sh
|   ├── docker_run_it.sh
|   ├── docker_run_server.sh
```

 * `img_db`: "database" which contains all users image uniquely by their id/name.

* `images`: "query" which contains all images need to find identity base on the simmilarity between it with the image in `img_db`,

 * Expects relative path to the query image in the same directory, otherwise provides absolute path.

* Edit [config.py](config.py) for your specific configuration. Otherwise leaves default.

## Run
1. Install dependencies
```
pip install -r requirements.txt
```

2. Run the server
```
uvicorn app.main:app --host 0.0.0.0 --port 80
```
* Add `--reload` flag to enable live mode.
* Go to `localhost:{port}/docs` for iterative API docs, check [doc](https://fastapi.tiangolo.com/#interactive-api-docs) for more information.

## Docker
Directory structure in docker's container:
```
├── /app
│   ├── app
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── utils.py
|   |
│   ├── data  # Database - Folder of images
│   │   ├── *.[jpg | jpeg]
|   |
│   ├── query  # Query - Folder of images need to find id
│   │   ├── *.[jpg | jpeg]
|   |
```
1. Pull [my repository](https://hub.docker.com/repository/docker/tiendang02/face-recognition-api/general).
```
docker pull tiendang02/face-recognition-api
```

2. Run the server

Run in Interative mode to test the api, forward to `localhost:80/docs`.
```
bash docker_run_it.sh
```

Run server non-interative mode after make sure of everything ;)
```
bash docker_run_server.sh
```
