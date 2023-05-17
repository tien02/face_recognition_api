### Model Config
# Get DeepFace configuration by setting index
# follow Model's Argument Options below
# Start at index 0
METRIC_ID = 2
MODEL_ID = 6
DETECTOR_ID = 4

### Data Config
DB_PATH = "app/data"  # relative path to images database (in this case is a folder of image)
RESIZE = False
SIZE = (300, 300)

#### -----------------!!!----------------- ###

### Model's Arguments Options
### DO NOT EDIT! ###
METRICS = [
  "cosine",   # 0
  "euclidean",  # 1
  "euclidean_l2"  # 2
  ]
MODELS = [
  "VGG-Face",   # 0
  "Facenet",  # 1
  "Facenet512",   # 2
  "OpenFace",   # 3
  "DeepFace",   # 4
  "DeepID",   # 5
  "ArcFace",  # 6
  "Dlib",   # 7
  "SFace",  # 8
]
DETECTORS = [
  'opencv',   # 0
  'ssd',  # 1
  'dlib',   # 2
  'mtcnn',  # 3
  'retinaface', # 4
  'mediapipe' # 5
]