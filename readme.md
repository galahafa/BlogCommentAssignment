
# Blog assignment

This project made as code test for interview.
you can create new post, add comment to this post, or add comment to comment.
get methods can return nested comment through 3 level.

### prepare to installation

make sure that you have docker/ docker-compose on your device

link to guide:
https://docs.docker.com/compose/install/

### installation

1) git clone this project
2) cd ./path-to-project
3) create .env file (or you can rename .env_example to .env)
4) docker-compose up --build -d
5) docker-compose run web python3 manage.py migrate


OpenApi available by swagger.yaml file or /swagger/ endpoint

