# Face Recognition API

## Tools
* Face Recognition model: [deepface](https://github.com/serengil/deepface)

* API: [fastapi](https://github.com/tiangolo/fastapi)

## Directory structure
This is how the project directory is structured:
```
├── app
│   ├── config.py
│   ├── main.py
│   └── utils.py
│   ├── data    # Database - Folder of images
│   │   ├── *.[jpg | jpeg]
|
├── query   # Query - Folder of images need to find id
│   ├── *.[jpg | jpeg]
|
├── docker-compose.yml
├── docker_build.sh
├── docker_run_it_test.sh
├── docker_run_server.sh
├── requirements.txt
└── uvicorn_run.sh
```

 * `data`: "database" which contains all users image uniquely by their id/name.

* `query`: "query" which contains all images need to find identity base on the simmilarity between it with the image in `database`

* I use [docker volume](https://docs.docker.com/storage/volumes/) to manage persistent data instead of using disk.

## Model configuration

* Face recognition model includes 2 modules: `face detection` and `face recognition`.

* For editting detector and recognizer configuration, see [config.py](config.py) for your specific configuration. Otherwise leaves as default.

## Run
1. Install dependencies
```
pip install -r requirements.txt
```
2. Create `./app/data` and `./query` as directory structure above.

3. Run the server
```
uvicorn app.main:app --host 0.0.0.0 --port 80
```
* Add `--reload` flag to enable live mode.
* Go to `localhost:{port}/docs` for [Swagger UI](https://swagger.io/tools/swagger-ui/), check [document](https://fastapi.tiangolo.com/#interactive-api-docs) for more information.

## Docker
Directory structure in docker container:
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

1. Run the service

```
docker compose up --build -d
```

2. Run manually

Build the image:
```
bash docker_build.sh
```

Run the container

```
bash docker_run_server.sh
```
