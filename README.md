# Python Application with Pipenv

This repository contains a Python application that can be run both as a Dockerized service and as a standalone service without Docker. The environment is managed using `pipenv`.

## Prerequisites  Running the Application without Docker

Before running the application, ensure you have the following requirements:

1. **Python**: You must have Python 3.9
2. **PostgreSQL Server installed and Database configured with acccess credentials**

# Applicatoin Deployment 

1. **Clone source code:**
   

2. **Pipenv** : Install `pipenv` . You can install it using `pip`:

   ```bash
   pip install pipenv
   ```
3. **Pipenv Dependencies**: Make environment and install dependencies:
   ```bash
   cd ecommer_app
   pipenv shell
   pipenv install
   ```
4. **Database Setup**: 
   It relies on a PostgreSQL database, make sure you have a PostgreSQL server running and provide the necessary database connection details in environment file.
         

5. **Environment Variables**:
   Application uses environment variables for configuration, rename the sample.env to .env file in the application root directory e.g. ~/app/.env . Please set the database connection paramets along with other requirements in .env file as environment variables. 
    
    
6. **Run Application**:After do above mention steps, run the following file.
   ```bash
    python main.py 
   ```

## Running the Application with Docker
**Prerequisites**
- Docker Engine & docker-compose must be installed
 
1. **Docker Image Build**: 
 Follow steps below
 - clone code to ~/app (command already shared above)
 - cd ~/app/
 - docker build -t app_api-v0.1.0 .
2. **Docker Run**:
 - docker run -it -p 8000:8000 -d app_api-v0.1.0:latest 
 
This Docker image is designed to run a Python application exposed on port 8000 and connect to a PostgreSQL database on port 5432.

## Run Migrations
1. **Run Migrations**: 
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   
   ```
2. **Run Application**:After do above mention steps, run the following file.
      ```bash
       python main.py 
      ```
3. **Database Credentials**: 
   It relies on a PostgreSQL database, make sure you have a PostgreSQL server running and provide the necessary database connection details in environment file.
4. user: admin
   password: Admin!123


