# Inventory Management System

This is a simple inventory management system implemented using FastAPI, Dapr, and Redis for pub/sub functionality.


## Overview

The inventory management system allows users to perform CRUD (Create, Read, Update, Delete) operations on inventory items. It uses a pub/sub architecture for event handling using Dapr and Redis.

## Project Structure

The project structure is as follows:


  
## Setup and Usage

1. Install the required dependencies using pip:

  command:
   pip install -r requirements.txt

Build the Docker image:

  command:
    docker build -t my-fastapi-app .

Run the Docker container:

command:
  docker run -d -p 80:80 inventory-management
  
The FastAPI application will be accessible at http://localhost:80.




License
This project is licensed under the MIT License.

