# biblion-management-system
A simple Book Management System

## Prerequisites
- docker

## Build & Run

Build a docker-image from the Dockerfile.
```bash
sudo docker build -t biblion_management_system .
```

Create a container from the generated docker-image and also start it.
```bash
sudo docker run -d --name bms_container -p 8000:8000 biblion_management_system
```

## Some useful docker commands
```bash
# to stop the container
sudo docker stop <container-name|conatiner-id>

# to remove the conatiner
sudo docker rm <container-name|conatiner-id>

# to remove the app image
sudo docker rmi <image-name|image-id>
```

> NOTE: A docker-image can only be deleted if there is no container using the image,
>        if a container uses the image but it is in stopped state, it
>        needs to be removed first in order to delete the image.


## Usage
Visit the [Documentation](http://127.0.0.1:8000/docs) to know, how:
- to create a new user.
- to Authorize the new user or login.
- to add a new book.
- to list all the books added by the current logged-in user.
- to get a single book by it's **id**.
- to update a book. and
- to delete a book.


# Linting and Formatting commands

poetry run ruff check --fix .
poetry run ruff format .

poetry run pylint $(git ls-files '*.py')
