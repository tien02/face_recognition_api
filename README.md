# Face Recognition API

## Tools
* Face Recognition model: [deepface](https://github.com/serengil/deepface)

* API: [fastapi](https://github.com/tiangolo/fastapi)

## Directory structure
Expects project's directory structure as:
```
├── project
│   ├── img_db
│   │   ├── *.[jpg | jpeg]
│   ├── main.py
│   ├── utils.py

```

 * Where `img_db` takes the role as "database" which contains all users image unique by their id/name.

 * Expects relative path to the query image in the same directory, otherwise provides absolute path.

* Edit [config.py](config.py) for your specific need. Otherwise leaves as default

## Run

1. Install dependencies
```
pip install -r requirements.txt
```

2. Run the server
```
uvicorn main:app --host 0.0.0.0 --port 80
```
* Add `--reload` flag to enable live mode.
* Go to `localhost:{port}/docs` for iterative API docs, check [doc](https://fastapi.tiangolo.com/#interactive-api-docs) for more information.