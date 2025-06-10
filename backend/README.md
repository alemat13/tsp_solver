# tsp_solver
TSP Solver (Travelling Salesman Problem)

## Prerequisites
You must install Docker Desktop :

https://www.docker.com/products/docker-desktop/

## Build Docker Image

The simpler way to build the Docker image is to run this command :

``docker build -t tsp_solver:latest https://github.com/alemat13/tsp_solver.git#main``

Or if you already cloned the repo, you can run the following command at the project root dir:

``docker build -t tsp_solver .``

## Run container

Then run the image :

``docker run -p 5000:5000 -t tsp_solver:latest``

## Access webapp

You can launch the webapp at the following address : http://127.0.0.1:5000

