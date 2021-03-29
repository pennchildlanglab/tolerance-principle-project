# Tolerance Principle Project

*Katie Schuler, Charles Yang, &  Elissa Newport*

## Project description

This repository contains an `experiments` directory (the experiment files) and an `analysis` directory (the data and analysis file).  NS(`data` directory), and analysis (`analysis` directory) for our manuscript "Testing the Tolerance Principle: Children form productive rules when it is more computationally efficient", submitted to the Journal of Memory and Language on March 29, 2021. 

## Analysis

You can clone this repository and start the project's analysis container to run the analysis. The only prerequisite is [Docker Desktop](https://www.docker.com/products/docker-desktop).

### Step 1: clone the repository

```
git clone https://github.com/pennchildlanglab/tolerance-principle-project.git
```

### Step 2: create an .env file

```
cd tolerance-principle-project
cp .env-sample .env
```

### Step 3: start the containers. From inside the project directory run:

``` 
docker-compose up -d --build
```

When the container is running, the analysis will be available at http://localhost:8989 (token = password). Files in the `analysis` directory are mapped to the `work` folder inside the container. When you've finished, you can stop the containers with:

```
docker-compose down
```




