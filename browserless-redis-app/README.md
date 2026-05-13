# Browser-less Redis Application

## Overview
This project is a browser-less application that utilizes Celery for asynchronous task processing and Redis as a message broker. The application is designed to handle tasks related to parsing movie data.

## Project Structure
```
browserless-redis-app
├── src
│   ├── parsing_movie
│   │   ├── celery
│   │   │   └── celery_app.py
│   │   └── __init__.py
│   └── __init__.py
├── Dockerfile.celery
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd browserless-redis-app
   ```

2. **Build the Docker Images**
   Use Docker Compose to build the images defined in the `docker-compose.yml` file.
   ```bash
   docker-compose build
   ```

3. **Run the Application**
   Start the services using Docker Compose.
   ```bash
   docker-compose up
   ```

## Usage
- The Celery worker will start processing tasks defined in `src/parsing_movie/celery/celery_app.py`.
- Ensure that Redis is running as defined in the `docker-compose.yml` file to facilitate message brokering.

## Dependencies
The project requires the following Python packages, which are listed in `requirements.txt`:
- Celery
- Redis
- Any additional libraries needed for browser-less functionality.

## Contributing
Feel free to submit issues or pull requests for improvements or bug fixes.