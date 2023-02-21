docker run -it --rm -p 80:80 \
--mount type=bind,source="$(pwd)"/img_db,target=/app/app/data \ # Database - Folder of images
--mount type=bind,source="$(pwd)"/images,target=/app/app/query \ # Query - Folder of images need to find id
face-recognition-api bash   