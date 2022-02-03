## Application Setup

This application consists of the following parts:

1. A FastAPI framework that serves as the REST API, responding to external requests. 
2. Celery is a task queue implementation for Python web applications used to asynchronously execute work outside the HTTP request-response cycle. It is used here to carry fetch data from the sse content that is given as background tasks. 
3. SQLAlchemy is used by Celery to consume data and process it. PostgreSQL is the database connector that is used.
4. Unit testing framework is used to construct the test for REST API.


## Getting started

The instruction given below will enable the application to run locally for testing purposes.

### Installation

#### Database Portion

1. Install the latest version of PostgreSQL. You can follow the steps provided in https://www.guru99.com/download-install-postgresql.html if you are on windows. This comes with pgAdmin.

2. Create user named 'postgres' with password being 'root'. These are the credentials that will be used for the database server.

3. Create two databases. One named "students" and the other named "teststudents"

#### Python dependecies 

Run the following command from the root directory:

```
pip install -r requirements.txt
```

### Dependencies

The dependencies used in this project are as follows:

```
celery==5.2.3
fastapi==0.72.0
Jinja2==3.0.3
psycopg2==2.9.3
pytest==6.2.5
requests==2.27.1
SQLAlchemy==1.4.31
sseclient==0.0.27
sseclient-py==1.7.2
ujson==4.3.0
urllib3==1.26.8
uvicorn==0.15.0

```

### Development

To start the server with live-reloading on code changes, please run:

```
uvicorn main.main:app --reload
```

On another window, start celery worker and watch their logs.  This worker is required to fetch data from the content-server:

```
celery -A main.main.celery worker --loglevel=info -P solo
```

After the application has started, the index page can be opened via http://127.0.0.1:8000/. As requested, the following endpoints are used:

http://127.0.0.1:8000/students
http://127.0.0.1:8000/students/{studentName} 
http://127.0.0.1:8000/exams
http://127.0.0.1:8000/exams/{examId}

The following endpoint comes predefined with the fastapi framework and it is documentation that
consists of the endpoints. You can also carry out execution of the endpoints:

http://127.0.0.1:8000/docs

### Testing

To execute the tests , please run the following from the root directory:

```
pytest
```