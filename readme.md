# Restaurant Open Hours API

This project provides an API for querying restaurant open hours based on a given date and time. It parses a dataset of restaurant names and their human-readable open hours, offering an endpoint to determine which restaurants are open at a specified datetime.

## Features

-   **API Endpoint**: Provides an endpoint to query restaurants open at a specific datetime.

-   **Dockerized Application**: Ensures easy setup and consistent runtime environment using Docker.

-   **Efficient Data Handling**: Utilizes interval trees for efficient querying of open hours.

-   **Comprehensive Test Suite**: Includes tests covering various scenarios, ensuring reliability.

## Note About Unknown Times

Some restaurants have unknown hours on certain days, even though it is known that they are open. A "\*" is appended to restaurant names in such cases.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. The project is containerized using Docker, which encapsulates its environment and dependencies for easy deployment.

### Prerequisites

-   Docker: The project is containerized, so you will need Docker installed on your system to build and run it. If you do not have Docker installed, please follow the [official Docker installation guide](https://docs.docker.com/get-docker/).

### Installing

1.  **Clone the Repository**: First, clone this repository to your local machine using Git.

```sh
git clone https://github.com/mvandoff/restaurant-open-hours-api
cd restaurant-open-hours-api
```

Or for SSH

```sh
git clone git@github.com:mvandoff/restaurant-open-hours-api
cd restaurant-open-hours-api
```

2.  **Build and Run with Docker Compose**: From the root of the cloned repository, run the following command to build the Docker image and start the container. This command also starts the API server.

`docker-compose up --build`

This command builds the Docker image based on the Dockerfile and `compose.yaml` configurations, installs any required dependencies, and starts the application. The API will be accessible at `http://localhost:8000`.

## Usage

Once the application is running, you can query the API to find out which restaurants are open at a specific datetime. Use the following endpoint format:

`GET /restaurants/open?datetime=YYYY-MM-DD HH:MM:SS`

Replace `YYYY-MM-DD HH:MM:SS` with the desired date and time. The API returns a JSON list of open restaurant names.

### Example Request

`curl http://localhost:8000/restaurants/open?datetime=2024-04-11 19:30:00`

### Response

The response will be a JSON list of restaurant names that are open at the specified datetime.

## Running Tests

To run the test suite and ensure the application functions as expected, execute the following command:

`docker-compose run --rm server python -m unittest`

This command runs the Python unittest module inside the Docker container, executing all tests defined in the `tests.py` file.
