# Inventory Management System

This is a simple inventory management system implemented using FastAPI, Dapr, and Redis for pub/sub functionality.


## Overview

The inventory management system allows users to perform CRUD (Create, Read, Update, Delete) operations on inventory items. It uses a pub/sub architecture for event handling using Dapr and Redis.

## Project Structure

The project structure is as follows:

- `app/`: Contains the main application files.
  - `main.py`: Implements the FastAPI application with CRUD endpoints and pub/sub event handlers using Dapr.
  - `dapr_client.py`: Includes the Dapr client code for interacting with Dapr runtime.
  - `models.py`: Defines Pydantic models for inventory items.
  - `requirements.txt`: Lists all Python dependencies required for the project.
  - `Dockerfile`: Contains instructions for building a Docker image for the FastAPI application.

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

Endpoints
POST /items/: Create a new inventory item.
GET /items/{item_id}: Retrieve details of a specific inventory item.
PUT /items/{item_id}: Update details of a specific inventory item.
DELETE /items/{item_id}: Delete a specific inventory item.
Pub/Sub Event Handlers
The project uses pub/sub event handlers for the following events:

item_created: Triggered when a new inventory item is created.
item_updated: Triggered when an existing inventory item is updated.


License
This project is licensed under the MIT License.

